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
from graphvex.explainability.explainer import (
    generate_explanation,
)


transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)


result = add_transaction_velocity(
    transactions,
    window_minutes=60,
)

result = add_amount_deviation(result)

result = high_velocity_rule(result)

result = unusual_amount_rule(result)

result = structuring_rule(result)


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

result = calculate_risk_score(result)


scenario_ids = [
    "CIRC0001",
    "RAPID0001",
    "STRUCT0003",
]


print("GRAPHVEX EXPLANATIONS")
print("=" * 60)


for transaction_id in scenario_ids:

    transaction = result[
        result["transaction_id"] == transaction_id
    ].iloc[0]

    explanation = generate_explanation(
        transaction
    )

    print()
    print("Transaction:", transaction_id)
    print("Risk score:", transaction["risk_score"])
    print("Explanation:", explanation)