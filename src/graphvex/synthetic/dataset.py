import pandas as pd
from datetime import datetime

from graphvex.synthetic.generator import (
    generate_customers,
    generate_transactions,
)
from graphvex.synthetic.labels import (
    GroundTruthLabel,
    label_normal_transactions,
    label_scenario_transactions,
)
from graphvex.synthetic.scenarios import (
    generate_circular_flow_scenario,
    generate_network_dispersion_scenario,
    generate_rapid_movement_scenario,
    generate_structuring_scenario,
)


def generate_dataset():
    """Generate the complete GraphVex synthetic dataset."""

    customers = generate_customers(
        count=100,
        seed=42,
    )

    normal_transactions = generate_transactions(
        customers=customers,
        count=1000,
        seed=42,
    )

    transactions = list(normal_transactions)

    ground_truth: list[GroundTruthLabel] = []

    ground_truth.extend(
        label_normal_transactions(
            [
                transaction.transaction_id
                for transaction in normal_transactions
            ]
        )
    )

    structuring = generate_structuring_scenario(
        sender_id="C0012",
        receiver_ids=[
            "C0041",
            "C0072",
            "C0033",
            "C0058",
        ],
        start_time=datetime(2026, 1, 15, 10, 0),
    )

    transactions.extend(structuring)

    ground_truth.extend(
        label_scenario_transactions(
            [tx.transaction_id for tx in structuring],
            "structuring",
        )
    )

    rapid_movement = generate_rapid_movement_scenario(
        account_ids=[
            "C0020",
            "C0040",
            "C0060",
            "C0080",
        ],
        start_time=datetime(2026, 1, 18, 11, 0),
    )

    transactions.extend(rapid_movement)

    ground_truth.extend(
        label_scenario_transactions(
            [tx.transaction_id for tx in rapid_movement],
            "rapid_movement",
        )
    )

    circular_flow = generate_circular_flow_scenario(
        account_ids=[
            "C0010",
            "C0020",
            "C0030",
            "C0040",
        ],
        start_time=datetime(2026, 1, 20, 14, 0),
    )

    transactions.extend(circular_flow)

    ground_truth.extend(
        label_scenario_transactions(
            [tx.transaction_id for tx in circular_flow],
            "circular_flow",
        )
    )

    network_dispersion = generate_network_dispersion_scenario(
        sender_id="C0050",
        receiver_ids=[
            "C0060",
            "C0070",
            "C0080",
            "C0090",
            "C0100",
        ],
        start_time=datetime(2026, 1, 25, 15, 0),
    )

    transactions.extend(network_dispersion)

    ground_truth.extend(
        label_scenario_transactions(
            [tx.transaction_id for tx in network_dispersion],
            "network_dispersion",
        )
    )

    return transactions, ground_truth


if __name__ == "__main__":
    transactions, ground_truth = generate_dataset()

    transaction_records = [
        transaction.model_dump()
        for transaction in transactions
    ]

    label_records = [
        label.__dict__
        for label in ground_truth
    ]

    transactions_df = pd.DataFrame(transaction_records)
    ground_truth_df = pd.DataFrame(label_records)

    transactions_df.to_parquet(
        "data/synthetic/transactions.parquet",
        index=False,
    )

    ground_truth_df.to_parquet(
        "data/synthetic/ground_truth.parquet",
        index=False,
    )

    print("Transactions:", len(transactions_df))
    print("Ground-truth labels:", len(ground_truth_df))
    print("Saved synthetic dataset.")