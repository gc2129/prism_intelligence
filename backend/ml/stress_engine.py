import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.metrics import accuracy_score, roc_auc_score

from correlation import (
    calculate_correlated_failures,
    print_correlation_report
)

from calibration import (
    calculate_calibration,
    print_calibration_report
)

from trust_score import (
    calculate_prism_trust_score,
    print_trust_report
)


# ---------------------------------
# PATH SETUP
# ---------------------------------

BASE_DIR = Path(__file__).parent.parent

DATA_PATH = BASE_DIR / "data" / "payment_data.csv"

MODELS_DIR = BASE_DIR / "models"


# ---------------------------------
# FEATURES
# ---------------------------------

FEATURES = [
    "transaction_amount",
    "transaction_velocity",
    "network_latency",
    "merchant_age_days",
    "geo_distance",
    "device_risk",
    "retry_count",
    "bank_latency",
    "hour_of_day",
    "merchant_risk"
]


# ---------------------------------
# TARGET MODELS
# ---------------------------------

TARGETS = {
    "fraud": "fraud_label",
    "routing": "routing_failure_label",
    "reliability": "reliability_failure_label"
}


# ---------------------------------
# LOAD MODELS
# ---------------------------------

def load_models():

    models = {}

    for name in TARGETS.keys():

        model_data = joblib.load(
            MODELS_DIR / f"{name}_model.pkl"
        )

        models[name] = model_data["model"]

    return models


# ---------------------------------
# EVALUATE MODELS
# ---------------------------------

def evaluate_models(df, models):

    results = {}

    X = df[FEATURES]

    for name, target_column in TARGETS.items():

        model = models[name]

        predictions = model.predict(X)

        probabilities = model.predict_proba(X)[:, 1]

        y_true = df[target_column]

        accuracy = accuracy_score(
            y_true,
            predictions
        )

        auc = roc_auc_score(
            y_true,
            probabilities
        )

        # Error pattern
        # 1 = incorrect prediction
        # 0 = correct prediction
        errors = (
            predictions != y_true
        ).astype(int)

        results[name] = {
            "accuracy": accuracy,
            "auc": auc,
            "predictions": predictions,
            "probabilities": probabilities,
            "errors": errors
        }

    return results


# ---------------------------------
# CREATE STRESS DATA
# ---------------------------------

def create_stress_data(df, stress_level=1.0):

    stressed = df.copy()

    np.random.seed(100)

    # Increase transaction velocity
    stressed["transaction_velocity"] = (
        stressed["transaction_velocity"]
        * (1 + 0.8 * stress_level)
    )

    # Increase network latency
    stressed["network_latency"] = (
        stressed["network_latency"]
        * (1 + 1.5 * stress_level)
    )

    # Increase bank latency
    stressed["bank_latency"] = (
        stressed["bank_latency"]
        * (1 + 1.2 * stress_level)
    )

    # Simulate unfamiliar merchant behaviour
    stressed["merchant_risk"] = np.clip(
        stressed["merchant_risk"]
        + np.random.normal(
            0.3 * stress_level,
            0.15,
            len(stressed)
        ),
        0,
        1
    )

    # Increase retry behaviour
    stressed["retry_count"] = np.clip(
        stressed["retry_count"]
        + np.random.poisson(
            2 * stress_level,
            len(stressed)
        ),
        0,
        10
    )

    # Geographic distribution shift
    stressed["geo_distance"] = (
        stressed["geo_distance"]
        * (1 + 1.0 * stress_level)
    )

    return stressed


# ---------------------------------
# LOCAL TESTING
# ---------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("PRISM ADVERSARIAL STRESS TEST")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)

    models = load_models()

    # Normal evaluation
    print("\nNORMAL CONDITIONS")

    normal_results = evaluate_models(
        df,
        models
    )

    for name, result in normal_results.items():

        print(
            f"{name.upper():15} "
            f"Accuracy: {result['accuracy']:.3f} | "
            f"AUC: {result['auc']:.3f}"
        )

    # Stress evaluation
    print("\n" + "=" * 60)
    print("STRESS CONDITIONS")
    print("=" * 60)

    stressed_df = create_stress_data(
        df,
        stress_level=1.0
    )

    stress_results = evaluate_models(
        stressed_df,
        models
    )

    for name, result in stress_results.items():

        print(
            f"{name.upper():15} "
            f"Accuracy: {result['accuracy']:.3f} | "
            f"AUC: {result['auc']:.3f}"
        )

    # Correlation analysis
    print("\n" + "=" * 60)
    print("NORMAL CONDITION CORRELATION")
    print("=" * 60)

    normal_correlation = calculate_correlated_failures(
        df,
        normal_results
    )

    print_correlation_report(
        normal_correlation
    )

    print("\n" + "=" * 60)
    print("STRESS CONDITION CORRELATION")
    print("=" * 60)

    stress_correlation = calculate_correlated_failures(
        stressed_df,
        stress_results
    )

    print_correlation_report(
        stress_correlation
    )

    # Calibration analysis
    normal_calibration = calculate_calibration(
        df,
        normal_results
    )

    stress_calibration = calculate_calibration(
        stressed_df,
        stress_results
    )

    print_calibration_report(
        normal_calibration,
        "NORMAL CONDITIONS"
    )

    print_calibration_report(
        stress_calibration,
        "STRESS CONDITIONS"
    )

    # Trust score
    normal_trust_score = calculate_prism_trust_score(
        normal_results,
        normal_calibration,
        normal_correlation
    )

    stress_trust_score = calculate_prism_trust_score(
        stress_results,
        stress_calibration,
        stress_correlation
    )

    print_trust_report(
        normal_trust_score,
        stress_trust_score
    )