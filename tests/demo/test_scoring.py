import pandas as pd

from graphvex.features.transaction_features import (
    add_amount_deviation,
    add_transaction_velocity,
)
from graphvex.graph.transaction_graph import (
    add_circular_flow_flags,
    detect_circular_flows,
)
from graphvex.rules.rules import (
    high_velocity_rule,
    structuring_rule,
    unusual_amount_rule,
)
from graphvex.scoring.risk_score import (
    calculate_risk_score,
)


transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

ground_truth = pd.read_parquet(
    "data/synthetic/ground_truth.parquet"
)


# -------------------------
# Feature engineering
# -------------------------

result = add_transaction_velocity(
    transactions,
    window_minutes=60,
)

result = add_amount_deviation(result)


# -------------------------
# Rule detection
# -------------------------

result = high_velocity_rule(result)

result = unusual_amount_rule(result)

result = structuring_rule(result)


# -------------------------
# Graph detection
# -------------------------

cycles = detect_circular_flows(
    transactions,
    max_cycle_length=6,
    max_duration_minutes=60,
    amount_tolerance=0.10,
)

result = add_circular_flow_flags(
    result,
    cycles,
)


# -------------------------
# Risk scoring
# -------------------------

result = calculate_risk_score(result)


# -------------------------
# Ground truth
# -------------------------

result = result.merge(
    ground_truth,
    on="transaction_id",
    how="left",
)


# -------------------------
# Display AML scenarios
# -------------------------

print("GRAPHVEX RISK SCORES")
print("=" * 60)

print(
    result[
        [
            "transaction_id",
            "scenario",
            "risk_score",
            "high_velocity_flag",
            "unusual_amount_flag",
            "structuring_flag",
            "circular_flow_flag",
        ]
    ]
    .query("scenario != 'normal'")
    .sort_values(
        ["scenario", "transaction_id"]
    )
    .to_string(index=False)
)