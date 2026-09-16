import pandas as pd

from graphvex.pipeline import run_pipeline


# Load data
transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

ground_truth = pd.read_parquet(
    "data/synthetic/ground_truth.parquet"
)


# Run GraphVex
result = run_pipeline(transactions)


# Add ground truth
result = result.merge(
    ground_truth,
    on="transaction_id",
    how="left",
)


# Ground-truth classification
result["actual_alert"] = (
    result["scenario"] != "normal"
)


# GraphVex classification
result["predicted_alert"] = (
    result["risk_score"] > 0
)


# Confusion matrix components
true_positive = (
    result["actual_alert"]
    & result["predicted_alert"]
).sum()

false_positive = (
    ~result["actual_alert"]
    & result["predicted_alert"]
).sum()

true_negative = (
    ~result["actual_alert"]
    & ~result["predicted_alert"]
).sum()

false_negative = (
    result["actual_alert"]
    & ~result["predicted_alert"]
).sum()


# Metrics
precision = (
    true_positive
    / (true_positive + false_positive)
    if true_positive + false_positive > 0
    else 0
)

recall = (
    true_positive
    / (true_positive + false_negative)
    if true_positive + false_negative > 0
    else 0
)

f1 = (
    2 * precision * recall
    / (precision + recall)
    if precision + recall > 0
    else 0
)


print("GRAPHVEX EVALUATION")
print("=" * 60)

print("\nConfusion Matrix")
print("-" * 30)

print("True positives :", true_positive)
print("False positives:", false_positive)
print("True negatives :", true_negative)
print("False negatives:", false_negative)

print("\nMetrics")
print("-" * 30)

print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"F1 score:  {f1:.3f}")


# Scenario-level results
print("\nScenario Detection")
print("-" * 30)

scenario_results = (
    result.groupby("scenario")
    .agg(
        transactions=("transaction_id", "count"),
        alerts=("predicted_alert", "sum"),
    )
)

scenario_results["alert_rate"] = (
    scenario_results["alerts"]
    / scenario_results["transactions"]
)

print(scenario_results)