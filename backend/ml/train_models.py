import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score


# Paths
BASE_DIR = Path(__file__).parent.parent

DATA_PATH = BASE_DIR / "data" / "payment_data.csv"
MODELS_DIR = BASE_DIR / "models"

MODELS_DIR.mkdir(exist_ok=True)


# Load dataset
df = pd.read_csv(DATA_PATH)


# Features used by all models
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


X = df[FEATURES]


# Labels
TARGETS = {
    "fraud": "fraud_label",
    "routing": "routing_failure_label",
    "reliability": "reliability_failure_label"
}


def train_model(name, target_column):
    print(f"\nTraining {name.upper()} model...")

    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Random Forest AI model
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, predictions)
    auc = roc_auc_score(y_test, probabilities)

    print(f"Accuracy: {accuracy:.3f}")
    print(f"ROC-AUC:  {auc:.3f}")

    # Save model
    model_path = MODELS_DIR / f"{name}_model.pkl"

    joblib.dump(
        {
            "model": model,
            "features": FEATURES,
            "accuracy": accuracy,
            "auc": auc
        },
        model_path
    )

    print(f"Saved: {model_path}")

    return {
        "accuracy": accuracy,
        "auc": auc
    }


if __name__ == "__main__":

    print("=" * 50)
    print("PRISM PAYMENT AI MODEL TRAINING")
    print("=" * 50)

    results = {}

    for model_name, target in TARGETS.items():
        results[model_name] = train_model(
            model_name,
            target
        )

    print("\n" + "=" * 50)
    print("TRAINING COMPLETE")
    print("=" * 50)

    for name, metrics in results.items():
        print(
            f"{name.upper():15} "
            f"Accuracy: {metrics['accuracy']:.3f} | "
            f"AUC: {metrics['auc']:.3f}"
        )