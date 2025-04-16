# __init__.py

def evaluate_cybersecurity_response(user_input, chatbot_response, log_analysis=None):
    # Se log_analysis non viene passato, prova ad estrarlo dalla chatbot_response
    if not log_analysis:
        required_sections = [
            "Risk Assessment",
            "MITRE ATT&CK Analysis",
            "Kill Chain Prediction",
            "Mitigation Strategy"
        ]
        if all(section in chatbot_response for section in required_sections):
            log_analysis = chatbot_response

    # Metriche base di qualità della risposta
    relevance = 1.0 if any(keyword in chatbot_response.lower() for keyword in user_input.lower().split()) else 0.6
    coherence = min(1.0, len(chatbot_response.split()) / 100)

    # Metriche di Trasparenza
    explainability = 1.0 if "MITRE ATT&CK" in chatbot_response or "CVE-" in chatbot_response else 0.5
    interpretability = 1.0 if len(chatbot_response.split()) <= 50 else 0.7

    # Metriche di Fairness
    non_discriminatory = 1.0
    rightful_info = 1.0 if any(ref in chatbot_response for ref in ["CVE", "CWE", "NIST", "MITRE"]) else 0.5

    # Metriche di Protection
    privacy_score = 1.0 if not any(pii in chatbot_response for pii in ["IP", "MAC", "username"]) else 0.3
    safety_score = 1.0 if "remediation" in chatbot_response.lower() or "mitigation" in chatbot_response.lower() else 0.5
    security_score = 1.0 if any(term in chatbot_response.lower() for term in ["patch", "update", "firewall"]) else 0.5

    # Valutazione approfondita dell'analisi di log
    log_analysis_score = 0
    completeness = 0
    accuracy = 0
    actionable = 0
    mitre_coverage = 0

    if log_analysis:
        # 1. Completezza della struttura
        required_sections = [
            "Risk Assessment",
            "MITRE ATT&CK Analysis",
            "Kill Chain Prediction",
            "Mitigation Strategy"
        ]
        completeness = sum(1 for section in required_sections if section in log_analysis) / len(required_sections)

        # 2. Accuratezza del contenuto
        risk_levels = ["Critical", "High", "Medium", "Low"]
        risk_present = any(level in log_analysis for level in risk_levels)
        mitre_present = "TA" in log_analysis and "T" in log_analysis

        accuracy = 0.6 if risk_present else 0.3
        accuracy += 0.4 if mitre_present else 0

        # 3. Azioni concrete
        has_immediate = "Immediate" in log_analysis and any(action in log_analysis for action in ["Block", "Isolate", "Disable"])
        has_long_term = "Long-term" in log_analysis and any(action in log_analysis for action in ["Patch", "Update", "Configure"])
        actionable = 0.5 * has_immediate + 0.5 * has_long_term

        # 4. Copertura MITRE ATT&CK (conta il numero di tecniche identificate)
        mitre_techniques = log_analysis.count("T") - log_analysis.count("TA")  # Stima approssimativa
        mitre_coverage = min(1.0, mitre_techniques / 3)  # Normalizzato su max 3 tecniche

        log_analysis_score = 0.3 * completeness + 0.3 * accuracy + 0.2 * actionable + 0.2 * mitre_coverage

    return {
        "transparency": {
            "explainability": explainability,
            "interpretability": interpretability,
            "score": 0.6 * explainability + 0.4 * interpretability
        },
        "fairness": {
            "non_discrimination": non_discriminatory,
            "rightful_information": rightful_info,
            "score": 0.3 * non_discriminatory + 0.7 * rightful_info
        },
        "protection": {
            "privacy": privacy_score,
            "safety": safety_score,
            "security": security_score,
            "score": 0.3 * privacy_score + 0.4 * safety_score + 0.3 * security_score
        },
        "log_analysis_quality": {
            "completeness": completeness if log_analysis else None,
            "accuracy": accuracy if log_analysis else None,
            "actionable": actionable if log_analysis else None,
            "mitre_coverage": mitre_coverage if log_analysis else None,
            "score": log_analysis_score if log_analysis else None
        },
        "basic_metrics": {
            "relevance": relevance,
            "coherence": coherence,
            "score": 0.6 * relevance + 0.4 * coherence
        },
        "overall_score": (
            0.15 * explainability +
            0.10 * rightful_info +
            0.20 * (0.4 * safety_score + 0.3 * security_score + 0.3 * privacy_score) +
            0.35 * (log_analysis_score if log_analysis else 0) +
            0.20 * relevance
        )
    }
