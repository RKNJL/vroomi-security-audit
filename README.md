![Python 3.10](https://img.shields.io/badge/python-3.10-blue)

# 🛡️ Vroomi AI Security Audit

> **A quantitative risk assessment of an AI assistant using Catastrophe Modeling and Contextual Mixture Distributions.**

Traditional risk models use **Average Loss** (Frequency × Impact). This fails for AI because most events are trivial but a few are catastrophic—and averaging hides the tail. This project replaces average-loss calculations with **Catastrophe Modeling** to expose the hidden risk that traditional models miss.

---

## 🔑 Key Findings

| Threat | Frequency | Financial Severity (P99) | Human Severity (P99) | Risk Rating |
|--------|-----------|--------------------------|----------------------|-------------|
| **Data Poisoning** | 5/yr | $5M+ | $10M+ | 🔴 Critical |
| **Sensitive Disclosure** | 40/yr | $100K+ | $500K+ | 🔴 Critical |
| **Misinformation** | 300/yr | $20K | $5M+ | 🟠 High |
| **Improper Output Handling** | 60/yr | $20K | $20K | 🟡 Medium |
| **Prompt Injection** | 150/yr | $100K | $1M | 🟡 Medium |
| **System Prompt Leak** | 20/yr | $10K | $200K | 🟢 Low |

**5 out of 6** threat categories were successfully exploited in the baseline Vroomi system.

---

## 🚀 Quick Start

### Run the Simulation

Run the following commands in your terminal:

`pip install numpy pandas scipy matplotlib`
`python src/ai_cat_mixture_model.py`

Output: `output/ai_cat_mixture_model.png` (4-panel risk visualization) and `output/ai_cat_mixture_model.csv` (raw data).

### Explore the Threat Map

Open `threat_map.html` in any browser for an interactive diagram of Vroomi's attack surface.

### Review the Notebooks

Each notebook in `notebooks/` contains an **attack demo** and a **defense demo** for one threat category:

| Notebook | Threat | What It Demonstrates |
|----------|--------|---------------------|
| `task_0_baseline` | Baseline | Vroomi's original (vulnerable) architecture |
| `task_1_prompt_injection` | Prompt Injection | User JSON bypasses model -> direct execution |
| `task_2_system_prompt_leak` | System Prompt Leak | Debug backdoor exposes internal prompt |
| `task_3_data_poisoning` | Data Poisoning | Fake document enters knowledge base unchecked |
| `task_4_sensitive_disclosure` | Sensitive Disclosure | PII in context window -> model reads it aloud |
| `task_5_misinformation` | Misinformation | Conflicting docs with no trust hierarchy |
| `task_6_improper_output_handling` | Improper Output | Model output executed without validation |

---

## 🧠 Methodology

### Why Catastrophe Modeling?

AI risks follow **power laws**, not bell curves. A single data poisoning event can be 10,000x worse than a typical one. Traditional models treat this as "average loss is acceptable." Our model treats it as "existential threat."

| Traditional Model | Our Model |
|---|---|
| "Average loss is $500K" | "95% of events cost <$1K, but 5% cost >$10M" |
| Decision: "Acceptable risk" | Decision: "Fix the tail immediately" |

### The Contextual Mixture Approach

Each threat is modeled as two states:

1. **Nuisance Mode** (95% of events): Low impact (e.g., wrong middle name on a badge)
2. **Catastrophe Mode** (5% of events): Massive impact (e.g., linking a victim to a crime)

The **Mixture Ratio** represents the probability that a successful attack escalates from nuisance to catastrophe. This captures the contextual variance that single-distribution models miss.

### Dual-Impact Analysis

We quantify both **Financial** and **Human** impact using:
- **Financial ALE**: Based on regulatory fines, operational downtime, and remediation costs
- **Human ALE**: Based on Weighted VSLY (Value of Statistical Life Year), a proxy for societal consequence used by the EPA, FDA, and DOT

Human harm is monetized not to price suffering, but to ensure it competes for resources alongside financial risk. Without a common unit, human impact is invisible in resource allocation.

### Key Metrics

| Metric | Meaning | Use Case |
|--------|---------|----------|
| **VaR 95%** | Worst case in a bad year (1-in-20) | Budgeting — how much reserve to set aside |
| **VaR 99%** | Catastrophe threshold (1-in-100) | Survival — can the organization withstand this? |
| **Tail Ratio** | VaR 99% / Mean | How "spiky" is the risk? Higher = more unpredictable |
| **Mixture Ratio** | % of events that are catastrophic | How often does a nuisance become a disaster? |

---

## 📊 Visualizations

| Chart | What It Shows |
|-------|--------------|
| **Bar Chart (Severity P99)** | Worst-case per-event impact for each threat |
| **Scatter Plot (Fin vs. Human)** | Dual-impact clustering — each dot is a threat, position shows catastrophe potential |
| **Tail Ratio Bar** | Spikiness of risk — higher bars mean the average hides extreme outcomes |
| **Radar Chart (Human Dimensions)** | Breakdown of harm types (privacy, safety, trust, autonomy, psychological) |
| **Summary Table** | Frequency, severity, ALE, and tail ratio for all threats |

---

## 🔧 Remediations

All remediation code is in `src/remediation.py`. Key fixes:

### P0 — Immediate

| Fix | Threats Addressed | What It Does |
|-----|-------------------|--------------|
| Delete `extract_forced_tool()` | Prompt Injection | Removes pre-model JSON parsing |
| Remove `DEBUG_MODE` branch | System Prompt Leak | Eliminates debug backdoor |
| Implement `get_safe_documents()` | Poisoning, Disclosure, Misinfo | Filters documents by trust/approval/sensitivity before context |

### P1 — High Priority

| Fix | Threats Addressed | What It Does |
|-----|-------------------|--------------|
| Add `validate_tool_call()` | Injection, Output Handling | Whitelist + type checking for tool calls |
| Add `verify_user_intent()` | Injection, Output Handling | Confirms user requested the action |
| Add `redact_pii()` | Sensitive Disclosure | Strips PII from model output |
| Add `validate_answer()` | Misinformation | Cross-checks output against trusted sources |

### P2 — Medium Priority

| Fix | Threats Addressed | What It Does |
|-----|-------------------|--------------|
| Add `detect_conflicts()` | Misinformation | Flags contradictory documents |
| Add confirmation step for destructive tools | Output Handling | Requires user OK before cancel/delete |
| Implement rate limiting | All | Caps tool calls per user session |
| Add logging + alerting | All | Tracks blocked actions and anomalies |

---

## 📚 Sources & Standards

This assessment is grounded in:

| Source | Usage |
|--------|-------|
| [ISO/IEC 23894:2023](https://www.iso.org/standard/77304.html) — AI Risk Management Guidance | Framework for AI-specific risk principles (dynamic, inclusive, best-available-information) |
| [OWASP Top 10 for LLMs (2023)](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Threat identification and ranking |
| [Cisco State of AI Security Report (2025)](https://www.cisco.com/c/en/us/products/security/state-of-ai-security-report.html) | Frequency estimation and threat landscape validation |
| [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) | Reliability and safety impact measurement |
| [MITRE ATLAS](https://atlas.mitre.org/) | Tactical attack lifecycle mapping |
| [Verizon DBIR 2024](https://www.verizon.com/business/resources/reports/dbir/) | Baseline social engineering and breach cost data |

---

## 📁 Repository Structure

vroomi-security-audit/
+-- README.md
+-- LICENSE
+-- src/
|   +-- ai_cat_mixture_model.py
|   +-- remediation.py
+-- notebooks/
|   +-- task_0_baseline.ipynb
|   +-- task_1_prompt_injection.ipynb
|   +-- task_2_system_prompt_leak.ipynb
|   +-- task_3_data_poisoning.ipynb
|   +-- task_4_sensitive_disclosure.ipynb
|   +-- task_5_misinformation.ipynb
|   +-- task_6_improper_output_handling.ipynb
+-- output/
|   +-- ai_cat_mixture_model.png
|   +-- ai_cat_mixture_model.csv
+-- docs/
|   +-- report.pdf
|   +-- appendix_b_methodology.md
+-- threat_map.html

---

## 📄 Appendix

For a detailed breakdown of the risk calculation methodology, frequency justification, and ethical considerations regarding human impact valuation, see:

👉 **[Appendix B: Risk Assessment Methodology](docs/appendix_b_methodology.md)**

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**[B Strassner]** — AI Security Capstone Project, April 2026

---

*"We replaced average-loss calculations with catastrophe modeling to expose the hidden tail risk that traditional models miss."*
