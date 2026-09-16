import pandas as pd

from graphvex.features.transaction_features import (
    add_transaction_velocity,
    add_amount_deviation,
)


transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

result = add_transaction_velocity(
    transactions,
    window_minutes=60,
)

result = add_amount_deviation(result)

scenario_ids = [
    "RAPID0001",
    "RAPID0002",
    "RAPID0003",
    "STRUCT0001",
    "STRUCT0002",
    "STRUCT0003",
    "STRUCT0004",
]

print(
    result[
        [
            "transaction_id",
            "sender_id",
            "amount",
            "sender_mean_amount",
            "sender_std_amount",
            "amount_zscore",
        ]
    ]
    .query("transaction_id in @scenario_ids")
    .sort_values("transaction_id")
)