def generate_incident_report(worst_scenario):
    """
    PRISM Incident Intelligence Engine

    Converts raw adversarial stress-test results into
    an interpretable engineering incident report.
    """

    stress_level = worst_scenario["stress_level"]
    trust_score = worst_scenario["trust_score"]
    correlation_rate = worst_scenario["correlated_failure_rate"] * 100

    # Severity reasoning
    if trust_score < 50 or correlation_rate > 25:
        severity = "CRITICAL"
        confidence = 0.96
    elif trust_score < 70 or correlation_rate > 18:
        severity = "HIGH"
        confidence = 0.92
    elif trust_score < 80 or correlation_rate > 12:
        severity = "MEDIUM"
        confidence = 0.86
    else:
        severity = "LOW"
        confidence = 0.78

    # Dynamic reasoning
    if correlation_rate > 18:
        hidden_pattern = (
            "Multiple AI decision systems are producing "
            "errors on overlapping transactions under stress."
        )
    else:
        hidden_pattern = (
            "Model failures remain mostly independent, "
            "but systemic coupling is beginning to emerge."
        )

    if stress_level >= 1.5:
        root_cause = (
            "High operational stress is amplifying shared "
            "failure conditions across multiple AI systems."
        )
    elif stress_level >= 1.2:
        root_cause = (
            "Moderate distribution shift is causing confidence "
            "degradation and increasing cross-model error overlap."
        )
    else:
        root_cause = (
            "Baseline model behavior is stable, but subtle "
            "correlation patterns require continued monitoring."
        )

    why_monitoring_missed_it = (
        "Traditional monitoring evaluates each model independently. "
        "Individual accuracy can remain stable while transaction-level "
        "errors become correlated across multiple decision systems."
    )

    if severity in ["CRITICAL", "HIGH"]:
        recommended_action = (
            "Add this adversarial scenario to the pre-deployment "
            "regression suite and introduce correlation-aware "
            "confidence monitoring."
        )
    else:
        recommended_action = (
            "Continue monitoring correlated error patterns and "
            "evaluate model independence under additional stress conditions."
        )

    return {
        "incident_id": f"PRISM-{int(stress_level * 100)}",
        "severity": severity,
        "confidence": confidence,
        "root_cause": root_cause,
        "hidden_pattern": hidden_pattern,
        "why_monitoring_missed_it": why_monitoring_missed_it,
        "recommended_action": recommended_action
    }