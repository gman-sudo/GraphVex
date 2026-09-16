import pandas as pd

from graphvex.pipeline import run_pipeline
from graphvex.scoring.customer_risk import (
    calculate_customer_risk,
)


# Load transactions
transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)


# Run transaction-level detection
result = run_pipeline(transactions)


# Calculate customer-level risk
customer_risk = calculate_customer_risk(result)


print("GRAPHVEX CUSTOMER RISK")
print("=" * 70)

print("\nCustomer count:")
print(len(customer_risk))


print("\nRisk level distribution:")
print(
    customer_risk["risk_level"]
    .value_counts()
    .sort_index()
)


print("\nHighest-risk customers:")
print(
    customer_risk[
        [
            "customer_id",
            "customer_risk_score",
            "risk_level",
            "total_alerts",
            "transactions_sent",
            "transactions_received",
        ]
    ]
    .sort_values(
        "customer_risk_score",
        ascending=False,
    )
    .head(15)
    .to_string(index=False)
)