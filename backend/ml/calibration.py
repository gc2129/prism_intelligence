import numpy as np
from sklearn.metrics import brier_score_loss


def calculate_ece(y_true, probabilities, n_bins=10):
    """
    Expected Calibration Error
    Measures difference between model confidence
    and actual correctness.
    """

    bin_boundaries = np.linspace(0, 1, n_bins + 1)

    ece = 0.0

    for i in range(n_bins):

        lower = bin_boundaries[i]
        upper = bin_boundaries[i + 1]

        mask = (
            (probabilities >= lower)
            & (probabilities < upper)
        )

        if np.sum(mask) == 0:
            continue

        bin_confidence = probabilities[mask].mean()
        bin_accuracy = y_true[mask].mean()

        bin_weight = np.sum(mask) / len(probabilities)

        ece += (
            bin_weight
            * abs(bin_accuracy - bin_confidence)
        )

    return float(ece)


def calculate_calibration(df, results):

    target_mapping = {
        "fraud": "fraud_label",
        "routing": "routing_failure_label",
        "reliability": "reliability_failure_label"
    }

    calibration_results = {}

    for model_name, target_column in target_mapping.items():

        y_true = df[target_column].values
        probabilities = results[model_name]["probabilities"]

        # Brier Score
        brier = brier_score_loss(
            y_true,
            probabilities
        )

        # Expected Calibration Error
        ece = calculate_ece(
            y_true,
            probabilities
        )

        # Average confidence
        confidence = np.maximum(
            probabilities,
            1 - probabilities
        ).mean()

        calibration_results[model_name] = {
            "brier_score": float(brier),
            "ece": float(ece),
            "average_confidence": float(confidence)
        }

    return calibration_results


def print_calibration_report(results, condition_name):

    print("\n" + "=" * 60)
    print(f"PRISM CALIBRATION ANALYSIS — {condition_name}")
    print("=" * 60)

    for model_name, metrics in results.items():

        print(f"\n{model_name.upper()} MODEL")

        print(
            f"Brier Score: "
            f"{metrics['brier_score']:.4f}"
        )

        print(
            f"ECE: "
            f"{metrics['ece']:.4f}"
        )

        print(
            f"Average Confidence: "
            f"{metrics['average_confidence'] * 100:.2f}%"
        )