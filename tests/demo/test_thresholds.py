import pandas as pd

from graphvex.pipeline import run_pipeline


# --------------------------------------------------
# Load data
# --------------------------------------------------

transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

ground_truth = pd.read_parquet(
    "data/synthetic/ground_truth.parquet"
)


# --------------------------------------------------
# Run GraphVex
# --------------------------------------------------

result = run_pipeline(transactions)


# --------------------------------------------------
# Add ground truth
# --------------------------------------------------

result = result.merge(
    ground_truth,
    on="transaction_id",
    how="left",
)


# --------------------------------------------------
# Define actual suspicious transactions
# --------------------------------------------------

result["actual_alert"] = (
    result["scenario"] != "normal"
)


# --------------------------------------------------
# Test different risk thresholds
# --------------------------------------------------

thresholds = [0, 20, 25, 30, 40, 45]


print("GRAPHVEX RISK THRESHOLD ANALYSIS")
print("=" * 70)


for threshold in thresholds:

    # Transactions above the threshold
    result["predicted_alert"] = (
        result["risk_score"] >= threshold
    )

    # Confusion matrix
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

    # Precision
    precision = (
        true_positive
        / (true_positive + false_positive)
        if true_positive + false_positive > 0
        else 0
    )

    # Recall
    recall = (
        true_positive
        / (true_positive + false_negative)
        if true_positive + false_negative > 0
        else 0
    )

    # F1
    f1 = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall > 0
        else 0
    )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print(f"\nThreshold >= {threshold}")
    print("-" * 40)

    print("Alerts        :", result["predicted_alert"].sum())
    print("True positives:", true_positive)
    print("False positives:", false_positive)
    print("True negatives:", true_negative)
    print("False negatives:", false_negative)

    print(f"Precision     : {precision:.3f}")
    print(f"Recall        : {recall:.3f}")
    print(f"F1 score      : {f1:.3f}")