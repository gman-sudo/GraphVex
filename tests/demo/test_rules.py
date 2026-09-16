import pandas as pd

from graphvex.features.transaction_features import (
    add_amount_deviation,
    add_transaction_velocity,
)
from graphvex.rules.rules import (
    high_velocity_rule,
    unusual_amount_rule,
    structuring_rule,
)


# Load synthetic dataset
transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

ground_truth = pd.read_parquet(
    "data/synthetic/ground_truth.parquet"
)


# Add behavioural features
result = add_transaction_velocity(
    transactions,
    window_minutes=60,
)

result = add_amount_deviation(result)


# Apply AML rules
result = high_velocity_rule(result)

result = unusual_amount_rule(result)

result = structuring_rule(result)


# Attach known ground-truth scenario labels
result = result.merge(
    ground_truth,
    on="transaction_id",
    how="left",
)


# Display suspicious scenarios
print(
    result[
        [
            "transaction_id",
            "scenario",
            "high_velocity_flag",
            "unusual_amount_flag",
            "structuring_flag",
        ]
    ]
    .query("scenario != 'normal'")
    .sort_values("transaction_id")
)

