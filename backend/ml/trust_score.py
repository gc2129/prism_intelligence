import numpy as np


def calculate_prism_trust_score(
    evaluation_results,
    calibration_results,
    correlation_report
):
    """
    Combines model performance, calibration quality,
    and systemic correlation risk into a 0-100 score.
    """

    # --------------------------------
    # 1. MODEL PERFORMANCE (40%)
    # --------------------------------

    accuracies = [
        evaluation_results[name]["accuracy"]
        for name in evaluation_results
    ]

    performance_score = np.mean(accuracies) * 100

    # --------------------------------
    # 2. CALIBRATION QUALITY (30%)
    # Lower Brier score = better
    # --------------------------------

    brier_scores = [
        calibration_results[name]["brier_score"]
        for name in calibration_results
    ]

    avg_brier = np.mean(brier_scores)

    calibration_score = (
        max(0, 1 - avg_brier)
        * 100
    )

    # --------------------------------
    # 3. CORRELATION RISK (30%)
    # Lower correlated failure = better
    # --------------------------------

    correlated_failure_rate = (
        correlation_report[
            "correlated_failure_rate"
        ]
    )

    correlation_score = (
        max(0, 1 - correlated_failure_rate * 5)
        * 100
    )

    # --------------------------------
    # FINAL PRISM SCORE
    # --------------------------------

    trust_score = (
        0.40 * performance_score
        + 0.30 * calibration_score
        + 0.30 * correlation_score
    )

    return {
        "trust_score": round(float(trust_score), 2),
        "performance_score": round(
            float(performance_score), 2
        ),
        "calibration_score": round(
            float(calibration_score), 2
        ),
        "correlation_score": round(
            float(correlation_score), 2
        )
    }


def get_trust_level(score):

    if score >= 85:
        return "HIGH TRUST"

    elif score >= 70:
        return "MODERATE TRUST"

    elif score >= 50:
        return "LOW TRUST"

    else:
        return "CRITICAL RISK"


def print_trust_report(
    normal_score,
    stress_score
):

    print("\n" + "=" * 60)
    print("PRISM TRUST INTELLIGENCE")
    print("=" * 60)

    print("\nNORMAL CONDITIONS")

    print(
        f"Trust Score: "
        f"{normal_score['trust_score']}/100"
    )

    print(
        f"Risk Level: "
        f"{get_trust_level(normal_score['trust_score'])}"
    )

    print("\nSTRESS CONDITIONS")

    print(
        f"Trust Score: "
        f"{stress_score['trust_score']}/100"
    )

    print(
        f"Risk Level: "
        f"{get_trust_level(stress_score['trust_score'])}"
    )

    print("\nTRUST SCORE CHANGE")

    difference = (
        stress_score["trust_score"]
        - normal_score["trust_score"]
    )

    print(
        f"Change: {difference:.2f}"
    )