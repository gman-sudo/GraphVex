import pandas as pd

from graphvex.graph.transaction_graph import (
    detect_circular_flows,
)


transactions = pd.read_parquet(
    "data/synthetic/transactions.parquet"
)

cycles = detect_circular_flows(
    transactions,
    max_cycle_length=6,
    max_duration_minutes=60,
    amount_tolerance=0.10,
)


print("CIRCULAR FLOW DETECTION")
print("=" * 40)

print("Detected:", len(cycles))

for cycle in cycles:

    if set(cycle["cycle"]) == {
        "C0010",
        "C0020",
        "C0030",
        "C0040",
    }:

        print("\nTARGET CYCLE FOUND")

        print(
            "Path:",
            " -> ".join(cycle["cycle"]),
        )

        print(
            "Transactions:",
            cycle["transaction_ids"],
        )

        print(
            "Amounts:",
            cycle["amounts"],
        )

        print(
            "Duration:",
            cycle["duration_minutes"],
            "minutes",
        )