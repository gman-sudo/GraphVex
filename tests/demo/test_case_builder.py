import pandas as pd

from graphvex.pipeline import run_pipeline
from graphvex.scoring.customer_risk import (
    calculate_customer_risk,
)
from graphvex.explainability.case_builder import (
    build_investigation_cases,
)


# Load transactions
transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)


# Run GraphVex
result = run_pipeline(transactions)


# Customer-level risk
customer_risk = calculate_customer_risk(
    result
)


# Build investigation cases
cases = build_investigation_cases(
    customer_risk
)


print("GRAPHVEX INVESTIGATION CASES")
print("=" * 70)

print("\nTotal cases:", len(cases))

print("\nCases:")
print(
    cases.to_string(index=False)
)