import numpy as np


def calculate_correlated_failures(df, results):
    """
    Detects transactions where 2 or more AI models
    make incorrect predictions simultaneously.
    """

    error_matrix = []

    model_names = [
        "fraud",
        "routing",
        "reliability"
    ]

    for name in model_names:

        target_column = {
            "fraud": "fraud_label",
            "routing": "routing_failure_label",
            "reliability": "reliability_failure_label"
        }[name]

        predictions = results[name]["predictions"]
        actual = df[target_column].values

        # 1 = model made an error
        errors = (predictions != actual).astype(int)

        error_matrix.append(errors)

    # Shape: transactions × models
    error_matrix = np.array(error_matrix).T

    # Number of models failing per transaction
    simultaneous_failures = error_matrix.sum(axis=1)

    # Correlated failure = 2 or more models fail together
    correlated_failure_mask = simultaneous_failures >= 2

    correlated_failure_rate = correlated_failure_mask.mean()

    # Pairwise error correlation
    correlation_matrix = np.corrcoef(
        error_matrix,
        rowvar=False
    )

    return {
        "correlated_failure_rate": correlated_failure_rate,
        "total_correlated_failures": int(
            correlated_failure_mask.sum()
        ),
        "total_transactions": len(df),
        "error_matrix": error_matrix,
        "simultaneous_failures": simultaneous_failures,
        "correlation_matrix": correlation_matrix
    }


def print_correlation_report(report):

    print("\n" + "=" * 60)
    print("PRISM CORRELATED FAILURE ANALYSIS")
    print("=" * 60)

    print(
        f"\nTotal Transactions: "
        f"{report['total_transactions']}"
    )

    print(
        f"Correlated Failure Events: "
        f"{report['total_correlated_failures']}"
    )

    print(
        f"Correlated Failure Rate: "
        f"{report['correlated_failure_rate'] * 100:.2f}%"
    )

    print("\nError Correlation Matrix:")
    print(report["correlation_matrix"])