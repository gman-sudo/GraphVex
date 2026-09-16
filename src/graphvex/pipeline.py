import pandas as pd

from graphvex.explainability.explainer import (
    generate_explanation,
)
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


def run_pipeline(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Run the complete GraphVex AML detection pipeline."""

    result = transactions.copy()

    # Feature engineering
    result = add_transaction_velocity(
        result,
        window_minutes=60,
    )

    result = add_amount_deviation(result)

    # Rule-based detection
    result = high_velocity_rule(result)

    result = unusual_amount_rule(result)

    result = structuring_rule(result)

    # Graph detection
    cycles = detect_circular_flows(
        result,
        max_cycle_length=6,
        max_duration_minutes=60,
        amount_tolerance=0.10,
    )

    result = add_circular_flow_flags(
        result,
        cycles,
    )

    # Risk scoring
    result = calculate_risk_score(result)

    # Explainability
    result["explanation"] = result.apply(
        generate_explanation,
        axis=1,
    )

    return result