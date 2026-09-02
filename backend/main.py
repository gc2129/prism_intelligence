import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["LOKY_MAX_CPU_COUNT"] = "1"

from fastapi.middleware.cors import CORSMiddleware
...
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pathlib import Path
import sys
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware



# ---------------------------------
# PATH SETUP
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(
    str(BASE_DIR / "ml")
)


# ---------------------------------
# IMPORTS
# ---------------------------------

from stress_engine import (
    load_models,
    create_stress_data,
    evaluate_models
)

from correlation import (
    calculate_correlated_failures
)

from pairwise_correlation import (
    calculate_pairwise_correlation
)

from calibration import (
    calculate_calibration
)

from trust_score import (
    calculate_prism_trust_score,
    get_trust_level
)

from red_team_agent import (
    run_red_team
)

from incident_engine import (
    generate_incident_report
)


# ---------------------------------
# FASTAPI APP
# ---------------------------------

app = FastAPI(
    title="PRISM API",
    description=(
        "AI Trust & Adversarial Intelligence "
        "for Payment Systems"
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://prism-intelligence-six.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------
# LOAD DATA + MODELS
# ---------------------------------

DATA_PATH = (
    BASE_DIR
    / "data"
    / "payment_data.csv"
)

df = pd.read_csv(DATA_PATH)

models = load_models()


# ---------------------------------
# HOME
# ---------------------------------

@app.get("/")
def home():

    return {
        "message": "PRISM backend is running",
        "status": "healthy"
    }


# ---------------------------------
# HEALTH
# ---------------------------------

@app.get("/health")
def health():

    return {
        "system": "PRISM",
        "status": "healthy",
        "models": [
            "Fraud Detection",
            "Routing Intelligence",
            "Reliability Prediction"
        ]
    }


# ---------------------------------
# DASHBOARD
# ---------------------------------

@app.get("/dashboard")
def dashboard():

    results = evaluate_models(
        df,
        models
    )

    correlation = (
        calculate_correlated_failures(
            df,
            results
        )
    )

    calibration = (
        calculate_calibration(
            df,
            results
        )
    )

    trust = (
        calculate_prism_trust_score(
            results,
            calibration,
            correlation
        )
    )

    model_metrics = {}

    for name, result in results.items():

        model_metrics[name] = {
            "accuracy": round(
                float(result["accuracy"]) * 100,
                2
            ),
            "auc": round(
                float(result["auc"]),
                3
            )
        }

    return {
        "trust_score": trust["trust_score"],

        "trust_level": get_trust_level(
            trust["trust_score"]
        ),

        "correlated_failure_rate": round(
            correlation[
                "correlated_failure_rate"
            ] * 100,
            2
        ),

        "total_transactions": correlation[
            "total_transactions"
        ],

        "model_metrics": model_metrics,

        "calibration": calibration
    }


# ---------------------------------
# STRESS TEST
# ---------------------------------

@app.get("/stress-test")
def stress_test(
    stress_level: float = 1.0
):

    stressed_df = (
        create_stress_data(
            df,
            stress_level=stress_level
        )
    )

    results = evaluate_models(
        stressed_df,
        models
    )

    correlation = (
        calculate_correlated_failures(
            stressed_df,
            results
        )
    )

    calibration = (
        calculate_calibration(
            stressed_df,
            results
        )
    )

    trust = (
        calculate_prism_trust_score(
            results,
            calibration,
            correlation
        )
    )

    return {
        "stress_level": stress_level,

        "trust_score": trust["trust_score"],

        "trust_level": get_trust_level(
            trust["trust_score"]
        ),

        "correlated_failure_rate": round(
            correlation[
                "correlated_failure_rate"
            ] * 100,
            2
        ),

        "performance": trust[
            "performance_score"
        ],

        "calibration": trust[
            "calibration_score"
        ],

       "correlation": round(
    correlation["correlated_failure_rate"],
    4
)
    }


# ---------------------------------
# AI RED TEAM
# ---------------------------------

@app.get("/red-team")
def red_team():

    worst_scenario, all_scenarios = (
        run_red_team(df)
    )

    incident = (
        generate_incident_report(
            worst_scenario
        )
    )

    return {
        "worst_scenario": {

            "scenario_id": worst_scenario[
                "scenario_id"
            ],

            "stress_level": worst_scenario[
                "stress_level"
            ],

            "trust_score": worst_scenario[
                "trust_score"
            ],

            "correlated_failure_rate": round(
                worst_scenario[
                    "correlated_failure_rate"
                ] * 100,
                2
            )
        },

        "incident": incident,

        "scenarios_tested": len(
            all_scenarios
        )
    }


# ---------------------------------
# CORRELATION INTELLIGENCE
# ---------------------------------

@app.get("/correlation-intelligence")
def correlation_intelligence(
    stress_level: float = 1.0
):

    # Normal conditions
    normal_results = (
        evaluate_models(
            df,
            models
        )
    )

    normal_correlations = (
        calculate_pairwise_correlation(
            normal_results
        )
    )

    # Stress conditions
    stressed_df = (
        create_stress_data(
            df,
            stress_level=stress_level
        )
    )

    stress_results = (
        evaluate_models(
            stressed_df,
            models
        )
    )

    stress_correlations = (
        calculate_pairwise_correlation(
            stress_results
        )
    )

    # Compare correlations
    comparison = []

    for normal, stressed in zip(
        normal_correlations,
        stress_correlations
    ):

        increase = (
            stressed["correlation"]
            - normal["correlation"]
        )

        comparison.append({

            "model_a":
                normal["model_a"],

            "model_b":
                normal["model_b"],

            "normal_correlation":
                normal["correlation"],

            "stress_correlation":
                stressed["correlation"],

            "correlation_change":
                round(
                    float(increase),
                    3
                ),

            "risk_level":
                stressed["risk_level"]
        })

    # Find strongest change
    highest_risk = max(
        comparison,
        key=lambda x: abs(
            x["correlation_change"]
        )
    )

    return {

        "analysis": (
            "PRISM Normal vs Stress "
            "Correlation Intelligence"
        ),

        "stress_level":
            stress_level,

        "comparison":
            comparison,

        "key_insight": {

            "models": (
                f"{highest_risk['model_a']} + "
                f"{highest_risk['model_b']}"
            ),

            "correlation_change":
                highest_risk[
                    "correlation_change"
                ],

            "risk_level":
                highest_risk[
                    "risk_level"
                ],

            "message": (
                "PRISM detected the strongest "
                "change in correlated failure "
                "behaviour under operational stress."
            )
        }
    }


# ---------------------------------
# TRUST HISTORY
# ---------------------------------

@app.get("/trust-history")
def trust_history():

    stress_levels = [
        0.5,
        1.2,
        2.0
    ]

    history = []

    for stress_level in stress_levels:

        # Create stressed environment
        stressed_df = (
            create_stress_data(
                df,
                stress_level=stress_level
            )
        )

        # Evaluate models
        results = (
            evaluate_models(
                stressed_df,
                models
            )
        )

        # Correlation analysis
        correlation = (
            calculate_correlated_failures(
                stressed_df,
                results
            )
        )

        # Calibration analysis
        calibration = (
            calculate_calibration(
                stressed_df,
                results
            )
        )

        # Trust score
        trust = (
            calculate_prism_trust_score(
                results,
                calibration,
                correlation
            )
        )

        history.append({

            "stress_level":
                stress_level,

            "trust_score":
                round(
                    float(
                        trust["trust_score"]
                    ),
                    2
                ),

            "correlated_failure_rate":
                round(
                    float(
                        correlation[
                            "correlated_failure_rate"
                        ]
                    ) * 100,
                    2
                ),

            "trust_level":
                get_trust_level(
                    trust["trust_score"]
                )
        })

    return {

        "analysis": (
            "PRISM Trust degradation "
            "under increasing operational stress"
        ),

        "history":
            history
    }