import pandas as pd

from graphvex.pipeline import run_pipeline
from graphvex.scoring.customer_risk import (
    calculate_customer_risk,
)
from graphvex.explainability.case_builder import (
    build_investigation_cases,
)


# ============================================================
# GraphVex AML Detection Demo
# ============================================================

print()
print("=" * 70)
print("GRAPHVEX AML DETECTION SYSTEM")
print("=" * 70)


# ------------------------------------------------------------
# 1. Load transactions
# ------------------------------------------------------------

transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

print()
print("Transactions loaded:", len(transactions))


# ------------------------------------------------------------
# 2. Run transaction-level detection
# ------------------------------------------------------------

result = run_pipeline(transactions)


# ------------------------------------------------------------
# 3. Calculate customer-level risk
# ------------------------------------------------------------

customer_risk = calculate_customer_risk(
    result
)


# ------------------------------------------------------------
# 4. Build investigation cases
# ------------------------------------------------------------

cases = build_investigation_cases(
    customer_risk
)


# ------------------------------------------------------------
# 5. Summary
# ------------------------------------------------------------

transaction_alerts = (
    result["risk_score"] > 0
).sum()

customers_with_risk = (
    customer_risk["customer_risk_score"] > 0
).sum()


print()
print("DETECTION SUMMARY")
print("-" * 70)

print(
    f"Transactions analysed : {len(result)}"
)

print(
    f"Transaction alerts    : {transaction_alerts}"
)

print(
    f"Customers analysed    : {len(customer_risk)}"
)

print(
    f"Customers requiring investigation : "
    f"{customers_with_risk}"
)


# ------------------------------------------------------------
# 6. Risk distribution
# ------------------------------------------------------------

print()
print("CUSTOMER RISK DISTRIBUTION")
print("-" * 70)

risk_distribution = (
    customer_risk["risk_level"]
    .value_counts()
    .reindex(
        ["critical", "high", "medium", "low"],
        fill_value=0,
    )
)

for level, count in risk_distribution.items():
    print(
        f"{level.capitalize():10} : {count}"
    )


# ------------------------------------------------------------
# 7. Investigation cases
# ------------------------------------------------------------

print()
print("INVESTIGATION CASES")
print("-" * 70)

print(
    cases[
        [
            "case_id",
            "customer_id",
            "customer_risk_score",
            "risk_level",
            "total_alerts",
            "reasons",
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 8. Top-risk case
# ------------------------------------------------------------

if not cases.empty:

    top_case = cases.iloc[0]

    print()
    print("TOP INVESTIGATION CASE")
    print("-" * 70)

    print(
        f"Case ID       : {top_case['case_id']}"
    )

    print(
        f"Customer      : {top_case['customer_id']}"
    )

    print(
        f"Risk score    : {top_case['customer_risk_score']}"
    )

    print(
        f"Risk level    : {top_case['risk_level']}"
    )

    print(
        f"Alert count   : {top_case['total_alerts']}"
    )

    print(
        f"Reasons       : {top_case['reasons']}"
    )

    print(
        f"Status        : {top_case['status']}"
    )


print()
print("=" * 70)
print("GRAPHVEX ANALYSIS COMPLETE")
print("=" * 70)
print()