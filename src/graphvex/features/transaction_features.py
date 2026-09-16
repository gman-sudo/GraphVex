import pandas as pd


def add_transaction_velocity(
    transactions: pd.DataFrame,
    window_minutes: int = 60,
) -> pd.DataFrame:
    """Add the number of outgoing transactions per sender within a time window."""

    df = transactions.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values(
        ["sender_id", "timestamp"]
    ).reset_index(drop=True)

    window = f"{window_minutes}min"

    df["transaction_velocity"] = (
        df.set_index("timestamp")
        .groupby("sender_id")["transaction_id"]
        .rolling(window)
        .count()
        .reset_index(level=0, drop=True)
        .to_numpy()
    )

    return df

def add_amount_deviation(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Add each transaction's deviation from the sender's average amount."""

    df = transactions.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    customer_stats = (
        df.groupby("sender_id")["amount"]
        .agg(["mean", "std"])
        .rename(
            columns={
                "mean": "sender_mean_amount",
                "std": "sender_std_amount",
            }
        )
    )

    df = df.join(
        customer_stats,
        on="sender_id",
    )

    df["amount_zscore"] = (
        (
            df["amount"]
            - df["sender_mean_amount"]
        )
        / df["sender_std_amount"]
    )

    df["amount_zscore"] = (
        df["amount_zscore"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    return df