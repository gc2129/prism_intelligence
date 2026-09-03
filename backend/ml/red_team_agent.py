import random
import pandas as pd

from stress_engine import (
    load_models,
    create_stress_data,
    evaluate_models
)

from correlation import calculate_correlated_failures
from calibration import calculate_calibration
from trust_score import calculate_prism_trust_score


def generate_attack_scenarios(n_scenarios=5):
    """
    AI agent generates different adversarial
    stress intensities to probe model blind spots.
    """

    scenarios = []

    for i in range(n_scenarios):

        stress_level = round(
            random.uniform(0.2, 2.0),
            2
        )

        scenarios.append({
            "scenario_id": i + 1,
            "stress_level": stress_level
        })

    return scenarios


def evaluate_scenario(df, models, scenario):

    stressed_df = create_stress_data(
        df,
        stress_level=scenario["stress_level"]
    )

    results = evaluate_models(
        stressed_df,
        models
    )

    correlation = calculate_correlated_failures(
        stressed_df,
        results
    )

    calibration = calculate_calibration(
        stressed_df,
        results
    )

    trust = calculate_prism_trust_score(
        results,
        calibration,
        correlation
    )

    return {
        "scenario_id": scenario["scenario_id"],
        "stress_level": scenario["stress_level"],
        "trust_score": trust["trust_score"],
        "correlated_failure_rate":
            correlation["correlated_failure_rate"],
        "results": results,
        "calibration": calibration,
        "correlation": correlation
    }


def run_red_team(df):

    print("\n" + "=" * 65)
    print("PRISM AI RED TEAM AGENT")
    print("=" * 65)

    models = load_models()

    scenarios = generate_attack_scenarios()

    evaluated_scenarios = []

    print(
        f"\nAgent generated {len(scenarios)} "
        f"adversarial scenarios..."
    )

    for scenario in scenarios:

        evaluation = evaluate_scenario(
            df,
            models,
            scenario
        )

        evaluated_scenarios.append(
            evaluation
        )

        print(
            f"Scenario {scenario['scenario_id']:02d} | "
            f"Stress: {scenario['stress_level']:.2f} | "
           f"Trust Score: {evaluation['trust_score']:.2f} | "
            f"Correlation Risk: "
            f"{evaluation['correlated_failure_rate'] * 100:.2f}%"
        )

    # Lowest trust score = worst discovered blind spot
    worst_scenario = min(
        evaluated_scenarios,
        key=lambda x: x["trust_score"]
    )

    return worst_scenario, evaluated_scenarios


if __name__ == "__main__":


    from pathlib import Path

    BASE_DIR = Path(__file__).parent.parent
    DATA_PATH = BASE_DIR / "data" / "payment_data.csv"

    df = pd.read_csv(DATA_PATH)

    worst_scenario, all_scenarios = run_red_team(df)
    from incident_engine import (
        generate_incident_report,
        print_incident_report
    )

    incident_report = generate_incident_report(
        worst_scenario
    )

    print_incident_report(
        incident_report
    )

    print("\n" + "=" * 65)
    print("🚨 BLIND SPOT DISCOVERED")
    print("=" * 65)

    print(
        f"\nWorst Scenario ID: "
        f"{worst_scenario['scenario_id']}"
    )

    print(
        f"Stress Level: "
        f"{worst_scenario['stress_level']}"
    )

    print(
        f"Trust Score: "
        f"{worst_scenario['trust_score']}/100"
    )

    print(
        f"Correlated Failure Rate: "
        f"{worst_scenario['correlated_failure_rate'] * 100:.2f}%"
    )

    print("\nPRISM Recommendation:")

    print(
        "This scenario should be investigated "
        "before deployment."
    )
