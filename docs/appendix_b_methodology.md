# Appendix B: Risk Assessment Methodology

## 1. Overview
This appendix details the methodology used to quantify the financial and human impact risks associated with the six identified AI threat vectors in the Vroomi Assistant system. The methodology is grounded in **ISO/IEC 23894:2023** (Information technology - Artificial intelligence - Guidance on risk management), which extends the generic risk management framework of ISO 31000:2018 with AI-specific considerations.

Given the nascent stage of AI-specific incident data, this assessment employs a **Relative Risk Scaling** approach, anchoring estimates to established cybersecurity frameworks, industry threat intelligence, and expert consensus from leading security organizations. This approach is consistent with ISO/IEC 23894:2023, Clause 4, Principle (f), which notes that "as AI is an emerging technology and constantly evolving, historical information can be limited, and future expectations can change quickly. Organizations should take this into account."

The methodology follows a **Qualitative-to-Quantitative** conversion process:
1.  **Threat Identification:** Based on the OWASP Top 10 for LLMs and MITRE ATLAS.
2.  **Frequency Estimation:** Derived from industry adoption rates, attack automation potential, and threat intelligence reports (Cisco, Verizon).
3.  **Impact Modeling:** Utilized **Catastrophe Modeling (Cat Modeling)** with Pareto distributions to capture "Black Swan" events, distinguishing between "Nuisance" (high frequency, low impact) and "Catastrophe" (low frequency, high impact) scenarios.
4.  **Dual-Impact Calculation:** Calculated both **Financial Annual Loss Expectancy (ALE)** and **Human Annual Loss Expectancy (ALE)** using a Weighted Value of Statistical Life Year (VSLY) framework.

## 2. Alignment with ISO/IEC 23894:2023 Principles
ISO/IEC 23894:2023, Table 1 defines several principles for AI risk management that directly inform this methodology:

| ISO/IEC 23894 Principle | Application in This Assessment |
| :--- | :--- |
| **(d) Inclusive:** "Organizations should seek dialog with diverse internal and external groups... to incorporate feedback and awareness into the risk management process." | The **Dual-Impact Model** (Financial + Human) ensures that non-financial stakeholder harms (privacy, safety, trust) are quantified alongside business losses, preventing a purely financial lens from obscuring societal impacts. |
| **(e) Dynamic:** "The nature of AI systems is itself dynamic, due to continuous learning, refining, evaluating, and validating... Dynamic risk management is particularly important for AI systems." | The **Contextual Mixture Model** captures the dynamic nature of AI risk by modeling each threat as a bimodal distribution (Nuisance vs. Catastrophe), reflecting how the same attack type can produce vastly different outcomes depending on context. |
| **(f) Best available information:** "Historical information can be limited, and future expectations can change quickly." | Frequency estimates are explicitly framed as **modeled scenarios** rather than empirical predictions, anchored to the best available industry data (Cisco 2025, OWASP, Verizon DBIR). All estimates include uncertainty ranges. |
| **(g) Human and cultural factors:** "Organizations should focus on identifying how AI systems interact with pre-existing societal patterns that can lead to impacts on equitable outcomes, privacy, freedom of expression, fairness, safety, security..." | The **Weighted VSLY** framework converts qualitative human harms (psychological harm, privacy violation, safety risk, trust erosion, autonomy violation) into quantifiable metrics, ensuring they are not dismissed as "intangible." |

## 3. Frequency Estimation Methodology
Exact historical frequencies for AI-specific attacks (e.g., prompt injections, data poisoning) are not yet publicly available in standardized databases. Consistent with ISO/IEC 23894:2023, Principle (f), frequencies were estimated using a **Relative Risk Scaling** methodology, calibrated against:
*   **OWASP Top 10 for LLMs (2023):** For threat ranking and attack surface analysis.
*   **Cisco State of AI Security Report (2025):** For current threat landscape validation and attack success rates.
*   **Verizon Data Breach Investigations Report (DBIR) 2024:** For baseline social engineering and credential compromise rates.
*   **MITRE ATLAS:** For tactical attack lifecycles.

### Frequency Justification Table

| Threat Vector | Est. Freq. (Events/Yr) | Primary Source & Justification |
| :--- | :--- | :--- |
| **Prompt Injection** | **150** | **Cisco (2025), p. 5-6:** Confirms that "simple jailbreaks continue to be effective against advances in AI safety" and that direct prompt injection is a primary attack vector. The high degree of automatability (similar to brute-force attacks) justifies the highest frequency estimate. |
| **Misinformation** | **300** | **NIST AI RMF (2023):** Highlights "Reliability" as a core risk. **Cisco (2025), p. 18:** Demonstrates that models can be tricked into regurgitating training data. As a probabilistic feature of LLMs, hallucinations occur at a rate proportional to usage volume, making this the most frequent event type. |
| **System Prompt Leak** | **20** | **Cisco (2025), p. 5:** Identifies prompt leakage as a specific consequence of jailbreaking. While common in research, in production it requires specific "extraction" attempts or debug backdoors, resulting in a lower frequency than general injection. |
| **Data Poisoning** | **5** | **Cisco (2025), p. 18:** Notes that poisoning web-scale datasets is "low-cost" ($60) but targets supply chains. For a specific enterprise RAG system, successful poisoning is a rare, high-effort supply chain attack, justifying a low-frequency estimate. |
| **Sensitive Disclosure** | **40** | **Cisco (2025), p. 19:** Explicitly lists "risk of sensitive data exposure" as a primary enterprise concern. **Verizon DBIR (2024):** Aligns with social engineering and accidental data exposure rates in cloud environments. |
| **Improper Output Handling** | **60** | **Cisco (2025), p. 10:** Highlights "Agentic AI" risks where agents "chain seemingly benign actions into harmful sequences." As tool usage increases, the frequency of unvalidated tool calls rises proportionally. |

## 4. Impact Modeling: Catastrophe & Mixture Distributions
Traditional risk models (Average Loss) fail to capture the "Black Swan" nature of AI risks. A single data poisoning event can be 10,000x more damaging than a typical prompt injection. To address this, we utilized **Catastrophe Modeling** with **Pareto Distributions** (Power Laws) to model the "heavy tail" of risk.

This approach is consistent with ISO/IEC 23894:2023, Principle (e), which emphasizes that "the nature of AI systems is itself dynamic" and that risk management should "anticipate, detect, acknowledge and respond to those changes and events in an appropriate and timely manner." Catastrophe modeling explicitly accounts for the dynamic, non-linear risk profile of AI systems.

### 4.1 The Mixture Model Approach
Each threat was modeled as a **Contextual Mixture** of two states:
1.  **Nuisance Mode:** High probability (95%+), low impact (e.g., a user asking for a refund that is denied).
2.  **Catastrophe Mode:** Low probability (<5%), massive impact (e.g., a poisoned policy causing mass financial fraud).

The **Mixture Ratio** (e.g., 5% for Misinformation, 20% for Data Poisoning) represents the probability that a successful attack escalates from a nuisance to a catastrophe. This ratio was derived from the **Cisco Report's** findings on the ease of breaking guardrails (p. 16) and the potential for "cascading effects" (p. 4).

### 4.2 Financial Impact (ALE)
Financial losses were modeled using **Triangular Distributions** for nuisance events and **Pareto Distributions** for catastrophic events.
*   **Parameters:** Min, Mode, and Max values were derived from industry benchmarks for similar incidents (e.g., GDPR fines for data leaks, operational downtime for ransomware).
*   **Source:** **Verizon DBIR 2024** for average breach costs; **Cisco (2025)** for AI-specific operational disruption scenarios.

### 4.3 Human Impact (ALE)
Human impact was quantified using a **Weighted Value of Statistical Life Year (VSLY)** framework, converting qualitative harm (privacy, safety, trust) into comparable dollar values. This approach directly addresses ISO/IEC 23894:2023, Principle (g), which requires organizations to "focus on identifying how AI systems interact with pre-existing societal patterns that can lead to impacts on equitable outcomes, privacy, freedom of expression, fairness, safety, security..."

*   **Methodology:** Each human impact dimension (Psychological Harm, Privacy Violation, Safety Risk, Trust Erosion, Autonomy Violation) was assigned a dollar weight based on health economics literature (EPA/HHS guidelines).
*   **Formula:** `Human ALE = Frequency x Probability x (Sum Dimension Weight x Severity Score)`
*   **Justification:** This approach aligns with **NIST AI RMF** guidelines for measuring "Safety" and "Fairness" impacts, ensuring that non-financial harms are not ignored in the risk calculation.

## 5. Risk Matrix & Classification
Risks were classified using a **Qualitative Risk Matrix** adapted from **ISO/IEC 23894:2023** and **OWASP Risk Rating Methodology**. The matrix structure follows the likelihood-impact framework described in ISO/IEC 23894:2023, Clause 6.4 (Risk Assessment), which defines risk evaluation as comparing risk levels against predefined criteria.

| Likelihood | Impact (Financial) | Impact (Human) | Overall Risk Rating |
| :--- | :--- | :--- | :--- |
| **High** (>100/yr) | Low | Low | **Medium** |
| **Medium** (10-100/yr) | Medium | High | **High** |
| **Low** (<10/yr) | High | High | **Critical** |

*   **Data Poisoning** is classified as **Critical** due to its low frequency but catastrophic potential (High-High).
*   **Prompt Injection** is classified as **High** due to its high frequency and moderate impact.
*   **Misinformation** is classified as **High** due to its very high frequency and high human impact (Trust Erosion).

## 6. Limitations & Future Work
Consistent with ISO/IEC 23894:2023, Principle (f), this assessment acknowledges that "historical information can be limited, and future expectations can change quickly." Specifically:

1.  **Frequency estimates** are modeled scenarios, not empirical observations. As AI incident databases mature (e.g., the AI Incident Database), these estimates should be recalibrated.
2.  **Mixture ratios** (Nuisance vs. Catastrophe) are expert judgments. Real-world deployment data should be used to validate these proportions.
3.  **Human impact weights** (VSLY) are derived from health economics, not AI-specific harm studies. As the field of AI safety matures, domain-specific harm metrics should replace generic VSLY proxies.
4.  **Dynamic risks** (Principle e) are not fully captured. The model treats each threat independently and does not model cascade effects (e.g., Data Poisoning -> Misinformation -> Public Panic). Future iterations should incorporate interdependency modeling.

## 7. References
1.  **ISO/IEC 23894:2023.** Information technology - Artificial intelligence - Guidance on risk management. International Organization for Standardization.
2.  **OWASP Foundation.** (2023). OWASP Top 10 for Large Language Model Applications. https://owasp.org/www-project-top-10-for-large-language-model-applications/
3.  **NIST.** (2023). AI Risk Management Framework (AI RMF 1.0). https://www.nist.gov/itl/ai-risk-management-framework
4.  **Cisco.** (2025). State of AI Security Report 2025. https://www.cisco.com/c/en/us/products/security/state-of-ai-security-report.html
5.  **Verizon.** (2024). Data Breach Investigations Report (DBIR 2024). https://www.verizon.com/business/resources/reports/dbir/
6.  **MITRE Corporation.** (2023). ATLAS: Adversarial Threat Landscape for Artificial-Intelligence Systems. https://atlas.mitre.org/
7.  **OWASP.** (2024). OWASP Risk Rating Methodology. https://owasp.org/www-community/OWASP_Risk_Rating_Methodology
