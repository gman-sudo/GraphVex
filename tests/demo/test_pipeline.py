import pandas as pd

from graphvex.pipeline import run_pipeline


transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

result = run_pipeline(transactions)


print("GRAPHVEX PIPELINE")
print("=" * 60)

print("Input transactions:", len(transactions))
print("Output transactions:", len(result))

print("\nRisk score distribution:")
print(
    result["risk_score"]
    .value_counts()
    .sort_index()
)

print("\nHighest-risk transactions:")

print(
    result[
        [
            "transaction_id",
            "risk_score",
            "explanation",
        ]
    ]
    .sort_values(
        "risk_score",
        ascending=False,
    )
    .head(15)
    .to_string(index=False)
)