import numpy as np


def calculate_pairwise_correlation(results):
    """
    Calculates pairwise correlation between model error patterns.

    If two models make mistakes on the same transactions,
    their error patterns will have a higher correlation.
    """

    model_names = list(results.keys())

    correlations = []

    for i in range(len(model_names)):
        for j in range(i + 1, len(model_names)):

            model_a = model_names[i]
            model_b = model_names[j]

            # Get error arrays
            errors_a = results[model_a]["errors"]
            errors_b = results[model_b]["errors"]

            # Correlation between failure patterns
            correlation = np.corrcoef(
                errors_a,
                errors_b
            )[0, 1]

            # Handle NaN
            if np.isnan(correlation):
                correlation = 0.0

            correlations.append({
                "model_a": model_a,
                "model_b": model_b,
                "correlation": round(float(correlation), 3),
                "risk_level": get_risk_level(correlation)
            })

    return correlations


def get_risk_level(correlation):

    correlation = abs(correlation)

    if correlation >= 0.40:
        return "HIGH"
    elif correlation >= 0.20:
        return "MEDIUM"
    else:
        return "LOW"