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

```bash
pip install numpy pandas scipy matplotlib
python src/ai_cat_mixture_model.py
