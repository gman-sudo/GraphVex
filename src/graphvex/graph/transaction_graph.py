import pandas as pd
import networkx as nx


def build_transaction_graph(
    transactions: pd.DataFrame,
) -> nx.MultiDiGraph:
    """Build a directed transaction graph.

    Nodes represent customers.
    Each transaction is represented as a separate directed edge.
    """

    graph = nx.MultiDiGraph()

    for _, transaction in transactions.iterrows():
        graph.add_node(transaction["sender_id"])
        graph.add_node(transaction["receiver_id"])

        graph.add_edge(
            transaction["sender_id"],
            transaction["receiver_id"],
            transaction_id=transaction["transaction_id"],
            amount=float(transaction["amount"]),
            timestamp=transaction["timestamp"],
        )

    return graph


def detect_circular_flows(
    transactions: pd.DataFrame,
    max_cycle_length: int = 6,
    max_duration_minutes: int = 60,
    amount_tolerance: float = 0.10,
) -> list[dict]:
    """Detect short, time-ordered circular money flows."""

    df = transactions.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df = df.sort_values("timestamp")

    detected = []

    for start_id, start_group in df.groupby("sender_id"):

        for _, start_tx in start_group.iterrows():

            path = [start_tx["sender_id"]]
            transactions_in_cycle = [start_tx]

            current_account = start_tx["receiver_id"]

            for _ in range(max_cycle_length - 1):

                candidates = df[
                    (df["sender_id"] == current_account)
                    & (
                        df["timestamp"]
                        >= transactions_in_cycle[-1]["timestamp"]
                    )
                ]

                if candidates.empty:
                    break

                next_tx = candidates.iloc[0]

                transactions_in_cycle.append(next_tx)
                path.append(next_tx["sender_id"])

                current_account = next_tx["receiver_id"]

                if current_account == start_tx["sender_id"]:

                    amounts = [
                        float(tx["amount"])
                        for tx in transactions_in_cycle
                    ]

                    mean_amount = sum(amounts) / len(amounts)

                    if mean_amount == 0:
                        break

                    deviations = [
                        abs(amount - mean_amount)
                        / mean_amount
                        for amount in amounts
                    ]

                    duration = (
                        transactions_in_cycle[-1]["timestamp"]
                        - transactions_in_cycle[0]["timestamp"]
                    ).total_seconds() / 60

                    if (
                        duration <= max_duration_minutes
                        and max(deviations) <= amount_tolerance
                    ):
                        detected.append(
                            {
                                "cycle": path + [
                                    start_tx["sender_id"]
                                ],
                                "transaction_ids": [
                                    tx["transaction_id"]
                                    for tx in transactions_in_cycle
                                ],
                                "amounts": amounts,
                                "duration_minutes": duration,
                            }
                        )

                    break

    return detected

def add_circular_flow_flags(
    transactions: pd.DataFrame,
    cycles: list[dict],
) -> pd.DataFrame:
    """Mark transactions that participate in detected circular flows."""

    df = transactions.copy()

    df["circular_flow_flag"] = False

    suspicious_transaction_ids = set()

    for cycle in cycles:
        suspicious_transaction_ids.update(
            cycle["transaction_ids"]
        )

    df.loc[
        df["transaction_id"].isin(
            suspicious_transaction_ids
        ),
        "circular_flow_flag",
    ] = True

    return df