import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from dataclasses import dataclass
from typing import Dict

@dataclass
class MixtureThreatProfile:
    name: str
    category: str
    annual_freq: float
    prob_alpha: float
    prob_beta: float
    
    # --- NUISANCE MODE (The "Middle Name on Badge" scenario) ---
    # Happens (1 - mixture_ratio) of the time
    nuisance_fin_scale: float
    nuisance_fin_shape: float
    nuisance_human_scale: float
    nuisance_human_shape: float
    
    # --- CATASTROPHE MODE (The "Linked to Crime" scenario) ---
    # Happens (mixture_ratio) of the time
    cat_fin_scale: float
    cat_fin_shape: float
    cat_human_scale: float
    cat_human_shape: float
    
    # Probability that a SUCCESSFUL attack is a CATASTROPHE (vs Nuisance)
    # e.g., 0.05 means 5% of successful attacks are catastrophic
    mixture_ratio: float 
    
    # Human Dimensions (for radar)
    dim_psych: float
    dim_privacy: float
    dim_safety: float
    dim_trust: float
    dim_autonomy: float
    
    description: str

# ==========================================
# 2. THREAT DEFINITIONS (WITH MIXTURES)
# ==========================================

THREATS = {
    "misinformation": MixtureThreatProfile(
        name="Misinformation",
        category="Reliability",
        annual_freq=300,
        prob_alpha=10, prob_beta=3,
        
        # NUISANCE: Wrong middle name on badge
        nuisance_fin_scale=10, nuisance_fin_shape=3.0,      # $10 min
        nuisance_human_scale=10, nuisance_human_shape=3.0,  # $10 min
        
        # CATASTROPHE: Linked to crime, defamation, suicide risk
        cat_fin_scale=50000, cat_fin_shape=1.5,             # $50k min, heavy tail
        cat_human_scale=1000000, cat_human_shape=1.2,       # $1M min, EXTREME tail
        
        mixture_ratio=0.05, # 5% of misinformation events are catastrophic
        
        dim_psych=6, dim_privacy=2, dim_safety=7, dim_trust=9, dim_autonomy=5,
        description="Mostly noise (bad badges), but 5% are life-destroying (false crimes)."
    ),
    
    "prompt_injection": MixtureThreatProfile(
        name="Prompt Injection",
        category="Integrity",
        annual_freq=150,
        prob_alpha=8, prob_beta=4,
        
        # NUISANCE: Joke, "tell me a joke" bypass
        nuisance_fin_scale=100, nuisance_fin_shape=3.0,
        nuisance_human_scale=100, nuisance_human_shape=3.0,
        
        # CATASTROPHE: Bypass safety to generate malware/terrorist plans
        cat_fin_scale=10000, cat_fin_shape=1.8,
        cat_human_scale=50000, cat_human_shape=1.6,
        
        mixture_ratio=0.02, # 2% are dangerous
        
        dim_psych=4, dim_privacy=3, dim_safety=5, dim_trust=6, dim_autonomy=7,
        description="Mostly harmless jokes, 2% generate dangerous content."
    ),

    "sensitive_info_disclosure": MixtureThreatProfile(
        name="Sensitive Info Disclosure",
        category="Confidentiality",
        annual_freq=15,
        prob_alpha=4, prob_beta=7,
        
        # NUISANCE: Leaks public info (phone number from directory)
        nuisance_fin_scale=1000, nuisance_fin_shape=2.5,
        nuisance_human_scale=1000, nuisance_human_shape=2.5,
        
        # CATASTROPHE: Leaks SSN, medical records, blackmail material
        cat_fin_scale=100000, cat_fin_shape=1.4,
        cat_human_scale=500000, cat_human_shape=1.3,
        
        mixture_ratio=0.10, # 10% are catastrophic
        
        dim_psych=6, dim_privacy=9, dim_safety=6, dim_trust=7, dim_autonomy=4,
        description="Mostly public data leaks, 10% are identity theft/blackmail."
    ),

    "data_poisoning": MixtureThreatProfile(
        name="Data Poisoning",
        category="Integrity",
        annual_freq=5,
        prob_alpha=5, prob_beta=8,
        
        # NUISANCE: Minor bias in recommendations
        nuisance_fin_scale=5000, nuisance_fin_shape=2.5,
        nuisance_human_scale=5000, nuisance_human_shape=2.5,
        
        # CATASTROPHE: Systemic failure, autonomous vehicle crash, medical misdiagnosis
        cat_fin_scale=5000000, cat_fin_shape=1.1,
        cat_human_scale=10000000, cat_human_shape=1.0,
        
        mixture_ratio=0.20, # 20% of poisoning events are catastrophic (high stakes)
        
        dim_psych=5, dim_privacy=5, dim_safety=8, dim_trust=9, dim_autonomy=7,
        description="Minor bias vs. Systemic collapse."
    ),
    
    # ... (Other threats can be added similarly, keeping them simple for now)
    "system_prompt_leak": MixtureThreatProfile(
        name="System Prompt Leak",
        category="Confidentiality",
        annual_freq=20,
        prob_alpha=6, prob_beta=5,
        nuisance_fin_scale=500, nuisance_fin_shape=3.0,
        nuisance_human_scale=500, nuisance_human_shape=3.0,
        cat_fin_scale=50000, cat_fin_shape=2.0,
        cat_human_scale=50000, cat_human_shape=2.0,
        mixture_ratio=0.05,
        dim_psych=2, dim_privacy=4, dim_safety=2, dim_trust=7, dim_autonomy=3,
        description="Leaking instructions."
    ),
    "improper_output_handling": MixtureThreatProfile(
        name="Improper Output Handling",
        category="Integrity",
        annual_freq=60,
        prob_alpha=5, prob_beta=6,
        nuisance_fin_scale=200, nuisance_fin_shape=3.0,
        nuisance_human_scale=200, nuisance_human_shape=3.0,
        cat_fin_scale=20000, cat_fin_shape=2.0,
        cat_human_scale=20000, cat_human_shape=2.0,
        mixture_ratio=0.05,
        dim_psych=3, dim_privacy=4, dim_safety=7, dim_trust=5, dim_autonomy=3,
        description="Minor formatting vs. SQL injection."
    ),
}

def run_mixture_simulation(threats, n_years=10000):
    results = []
    print(f"Running Mixture Simulation ({n_years:,} years)...")

    for key, cfg in threats.items():
        annual_losses_fin = []
        annual_losses_human = []
        per_event_fin = []
        per_event_human = []

        for _ in range(n_years):
            num_attempts = np.random.poisson(cfg.annual_freq)
            if num_attempts == 0:
                annual_losses_fin.append(0)
                annual_losses_human.append(0)
                continue

            # 1. Success Probability
            success_probs = np.random.beta(cfg.prob_alpha, cfg.prob_beta, num_attempts)
            successes = (np.random.rand(num_attempts) < success_probs).sum()
            
            if successes == 0:
                annual_losses_fin.append(0)
                annual_losses_human.append(0)
                continue

            # 2. Determine Mode: Nuisance vs Catastrophe
            # For each successful event, roll the dice: Is it a catastrophe?
            is_catastrophe = (np.random.rand(successes) < cfg.mixture_ratio)
            
            # 3. Sample Losses based on Mode
            # Nuisance losses
            n_count = np.sum(~is_catastrophe)
            if n_count > 0:
                n_fin = stats.pareto.rvs(b=cfg.nuisance_fin_shape, scale=cfg.nuisance_fin_scale, size=n_count)
                n_human = stats.pareto.rvs(b=cfg.nuisance_human_shape, scale=cfg.nuisance_human_scale, size=n_count)
            else:
                n_fin, n_human = np.array([]), np.array([])

            # Catastrophe losses
            c_count = np.sum(is_catastrophe)
            if c_count > 0:
                c_fin = stats.pareto.rvs(b=cfg.cat_fin_shape, scale=cfg.cat_fin_scale, size=c_count)
                c_human = stats.pareto.rvs(b=cfg.cat_human_shape, scale=cfg.cat_human_scale, size=c_count)
            else:
                c_fin, c_human = np.array([]), np.array([])

            # Combine
            all_fin = np.concatenate([n_fin, c_fin])
            all_human = np.concatenate([n_human, c_human])

            per_event_fin.extend(all_fin.tolist())
            per_event_human.extend(all_human.tolist())

            annual_losses_fin.append(np.sum(all_fin))
            annual_losses_human.append(np.sum(all_human))

        arr_fin = np.array(annual_losses_fin)
        arr_human = np.array(annual_losses_human)
        arr_ev_fin = np.array(per_event_fin) if per_event_fin else np.array([0])
        arr_ev_human = np.array(per_event_human) if per_event_human else np.array([0])

        results.append({
            'Threat': cfg.name,
            'Category': cfg.category,
            'Annual_Freq': cfg.annual_freq,
            'Mixture_Ratio': cfg.mixture_ratio,
            # Per-Event Severity (The Key Metric)
            'Sev_Fin_Mean': np.mean(arr_ev_fin),
            'Sev_Fin_P95': np.percentile(arr_ev_fin, 95),
            'Sev_Fin_P99': np.percentile(arr_ev_fin, 99),
            'Sev_Human_Mean': np.mean(arr_ev_human),
            'Sev_Human_P95': np.percentile(arr_ev_human, 95),
            'Sev_Human_P99': np.percentile(arr_ev_human, 99),
            # Annual Aggregate
            'ALE_Fin': np.mean(arr_fin),
            'ALE_Human': np.mean(arr_human),
            'Tail_Ratio': np.percentile(arr_fin, 99) / max(np.mean(arr_fin), 1),
            # Dimensions
            'Dim_Psych': cfg.dim_psych,
            'Dim_Privacy': cfg.dim_privacy,
            'Dim_Safety': cfg.dim_safety,
            'Dim_Trust': cfg.dim_trust,
            'Dim_Autonomy': cfg.dim_autonomy,
            'Description': cfg.description,
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by='Sev_Fin_P99', ascending=False).reset_index(drop=True)
    return df

def plot_mixture_model(df):
    fig = plt.figure(figsize=(18, 14))

    # ---- PANEL 1: Severity P99 (The "Worst Case" View) ----
    ax1 = fig.add_subplot(2, 2, 1)
    threats = df['Threat'].tolist()
    x = np.arange(len(threats))
    width = 0.35

    sev_fin_log = np.log10(df['Sev_Fin_P99'].clip(1))
    sev_human_log = np.log10(df['Sev_Human_P99'].clip(1))

    ax1.bar(x - width/2, sev_fin_log, width, label='Financial Severity P99', color='#e74c3c', alpha=0.8)
    ax1.bar(x + width/2, sev_human_log, width, label='Human Severity P99', color='#3498db', alpha=0.8)

    ax1.set_ylabel('Log₁₀ Per-Event Loss ($)')
    ax1.set_title('Per-Event Severity at 99th Percentile\n(Captures the "Catastrophe" Tail)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(threats, rotation=30, ha='right', fontsize=8)
    ax1.legend(fontsize=8)
    ax1.grid(axis='y', alpha=0.3)

    # Add Mixture Ratio labels
    for i, row in df.iterrows():
        ratio = row['Mixture_Ratio']
        ax1.text(i, max(sev_fin_log.iloc[i], sev_human_log.iloc[i]) + 0.1, 
                 f'{ratio*100:.0f}% Cat', ha='center', fontsize=7, fontweight='bold', color='#2c3e50')

    # ---- PANEL 2: Severity Scatter (Log-Log) ----
    ax2 = fig.add_subplot(2, 2, 2)

    scatter = ax2.scatter(
        df['Sev_Fin_P99'], df['Sev_Human_P99'],
        s=200, c=df['Mixture_Ratio'], cmap='YlOrRd',
        edgecolors='black', alpha=0.8, linewidth=1.5
    )

    for i, row in df.iterrows():
        ax2.annotate(row['Threat'],
                     (row['Sev_Fin_P99'], row['Sev_Human_P99']),
                     fontsize=9, fontweight='bold',
                     xytext=(8, 8), textcoords='offset points',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

    ax2.set_xlabel('Financial Severity P99 ($)')
    ax2.set_ylabel('Human Severity P99 ($)')
    ax2.set_title('Per-Event Catastrophe Potential\n(Color = % of Events that are Catastrophic)')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, which='both')
    plt.colorbar(scatter, ax=ax2, label='% Catastrophic Events')

    fin_med = df['Sev_Fin_P99'].median()
    human_med = df['Sev_Human_P99'].median()
    ax2.axvline(x=fin_med, color='gray', linestyle='--', alpha=0.6)
    ax2.axhline(y=human_med, color='gray', linestyle='--', alpha=0.6)

    ax2.text(0.02, 0.98, 'Low Fin / High Human', transform=ax2.transAxes, fontsize=9, va='top', color='blue', fontweight='bold')
    ax2.text(0.98, 0.98, 'High Fin / High Human', transform=ax2.transAxes, fontsize=9, va='top', ha='right', color='red', fontweight='bold')
    ax2.text(0.02, 0.02, 'Low Fin / Low Human', transform=ax2.transAxes, fontsize=9, va='bottom', color='gray', fontweight='bold')
    ax2.text(0.98, 0.02, 'High Fin / Low Human', transform=ax2.transAxes, fontsize=9, va='bottom', ha='right', color='orange', fontweight='bold')

    # ---- PANEL 3: Nuisance vs Catastrophe Split ----
    ax3 = fig.add_subplot(2, 2, 3)
    # Calculate the ratio of P99 to Mean to show how "fat" the tail is
    # A high ratio means the P99 is much higher than the average (i.e., mostly nuisance, rare catastrophe)
    tail_intensity = df['Sev_Fin_P99'] / df['Sev_Fin_Mean']
    
    ax3.barh(range(len(df)), tail_intensity, color='#9b59b6', alpha=0.8)
    ax3.set_yticks(range(len(df)))
    ax3.set_yticklabels(df['Threat'])
    ax3.set_xlabel('Tail Intensity (P99 / Mean)')
    ax3.set_title('How "Spiky" is the Risk?\n(High = Mostly Nuisance, Rare Catastrophe)')
    ax3.grid(axis='x', alpha=0.3)
    
    for i, v in enumerate(tail_intensity):
        ax3.text(v + 0.5, i, f'{v:.1f}x', va='center', fontsize=8)

    # ---- PANEL 4: Summary Table ----
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis('off')

    table_data = []
    for _, row in df.iterrows():
        table_data.append([
            row['Threat'],
            f"{row['Mixture_Ratio']*100:.0f}% Cat",
            f"${row['Sev_Fin_P99']:,.0f}",
            f"${row['Sev_Human_P99']:,.0f}",
            f"${row['ALE_Fin']:,.0f}",
            f"{row['Tail_Ratio']:.1f}x",
        ])

    col_labels = ['Threat', '% Catastrophe', 'Sev Fin P99', 'Sev Human P99', 'ALE Fin', 'Tail']
    table = ax4.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.0, 1.5)

    for j in range(len(col_labels)):
        table[0, j].set_facecolor('#2c3e50')
        table[0, j].set_text_props(color='white', fontweight='bold')

    for i in range(1, len(table_data) + 1):
        if i % 2 == 0:
            for j in range(len(col_labels)):
                table[i, j].set_facecolor('#f2f2f2')

    plt.tight_layout()
    plt.savefig('ai_cat_mixture_model.png', dpi=300, bbox_inches='tight')
    print("Charts saved as 'ai_cat_mixture_model.png'")
    plt.show()

if __name__ == "__main__":
    try:
        results_df = run_mixture_simulation(THREATS, n_years=10000)

        print("\n" + "="*80)
        print("AI SECURITY AUDIT: CONTEXTUAL MIXTURE MODEL")
        print("="*80)
        print(results_df[['Threat', 'Mixture_Ratio', 'Sev_Fin_P99', 'Sev_Human_P99', 'ALE_Fin', 'Tail_Ratio']].to_string(index=False))
        print("="*80)
        print("\nNote: 'Mixture Ratio' is the % of events that are 'Catastrophic'.")
        print("      P99 captures the worst 1% of events (the Catastrophes).")
        print("      ALE captures the average (dominated by Nuisances).")
        print("="*80)

        plot_mixture_model(results_df)

        results_df.to_csv('ai_cat_mixture_model.csv', index=False)
        print("CSV saved.")

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
