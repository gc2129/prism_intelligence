import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

N_SAMPLES = 10000


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_payment_data(n_samples=N_SAMPLES):
    # Transaction features
    transaction_amount = np.random.lognormal(mean=7.5, sigma=1.0, size=n_samples)
    transaction_amount = np.clip(transaction_amount, 50, 200000)

    transaction_velocity = np.random.poisson(lam=5, size=n_samples)

    network_latency = np.random.normal(
        loc=250, scale=120, size=n_samples
    )
    network_latency = np.clip(network_latency, 20, 2000)

    merchant_age_days = np.random.exponential(
        scale=800, size=n_samples
    )
    merchant_age_days = np.clip(merchant_age_days, 1, 5000)

    geo_distance = np.random.exponential(
        scale=50, size=n_samples
    )
    geo_distance = np.clip(geo_distance, 0, 2000)

    device_risk = np.random.beta(
        a=2, b=5, size=n_samples
    )

    retry_count = np.random.poisson(
        lam=0.8, size=n_samples
    )
    retry_count = np.clip(retry_count, 0, 10)

    bank_latency = np.random.normal(
        loc=180, scale=80, size=n_samples
    )
    bank_latency = np.clip(bank_latency, 20, 1500)

    hour_of_day = np.random.randint(
        0, 24, size=n_samples
    )

    # Merchant category encoded as numeric risk
    merchant_risk = np.random.beta(
        a=2, b=4, size=n_samples
    )

    # -----------------------------
    # Generate realistic labels
    # -----------------------------

    # FRAUD RISK
    fraud_score = (
        0.00003 * transaction_amount
        + 0.12 * transaction_velocity
        + 2.0 * device_risk
        + 0.001 * geo_distance
        + 1.5 * merchant_risk
        + np.random.normal(0, 0.8, n_samples)
        - 3.5
    )

    fraud_probability = sigmoid(fraud_score)
    fraud_label = (fraud_probability > 0.5).astype(int)

    # ROUTING FAILURE RISK
    routing_score = (
        0.002 * network_latency
        + 0.002 * bank_latency
        + 0.25 * retry_count
        + 0.05 * transaction_velocity
        + 1.2 * merchant_risk
        + np.random.normal(0, 0.7, n_samples)
        - 2.2
    )

    routing_probability = sigmoid(routing_score)
    routing_label = (routing_probability > 0.5).astype(int)

    # RELIABILITY FAILURE RISK
    reliability_score = (
        0.0015 * network_latency
        + 0.0015 * bank_latency
        + 0.18 * retry_count
        + 0.8 * device_risk
        + 0.0005 * transaction_amount
        + np.random.normal(0, 0.7, n_samples)
        - 2.5
    )

    reliability_probability = sigmoid(reliability_score)
    reliability_label = (reliability_probability > 0.5).astype(int)

    # Create DataFrame
    df = pd.DataFrame({
        "transaction_amount": transaction_amount.round(2),
        "transaction_velocity": transaction_velocity,
        "network_latency": network_latency.round(2),
        "merchant_age_days": merchant_age_days.round(2),
        "geo_distance": geo_distance.round(2),
        "device_risk": device_risk.round(3),
        "retry_count": retry_count,
        "bank_latency": bank_latency.round(2),
        "hour_of_day": hour_of_day,
        "merchant_risk": merchant_risk.round(3),

        "fraud_label": fraud_label,
        "routing_failure_label": routing_label,
        "reliability_failure_label": reliability_label
    })

    return df


if __name__ == "__main__":
    df = generate_payment_data()

    output_path = Path(__file__).parent.parent / "data" / "payment_data.csv"

    df.to_csv(output_path, index=False)

    print("Dataset generated successfully!")
    print(f"Total transactions: {len(df)}")
    print(f"Saved to: {output_path}")

    print("\nLabel distribution:")
    print(df[
        [
            "fraud_label",
            "routing_failure_label",
            "reliability_failure_label"
        ]
    ].mean())