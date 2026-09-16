import pandas as pd


def high_velocity_rule(
    transactions: pd.DataFrame,
    threshold: int = 3,
) -> pd.DataFrame:
    """Flag transactions occurring during unusually high velocity."""

    df = transactions.copy()

    df["high_velocity_flag"] = (
        df["transaction_velocity"] >= threshold
    )

    return df


def unusual_amount_rule(
    transactions: pd.DataFrame,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """Flag transactions with unusually high amount deviation."""

    df = transactions.copy()

    df["unusual_amount_flag"] = (
        df["amount_zscore"].abs() >= threshold
    )

    return df

def structuring_rule(
    transactions: pd.DataFrame,
    min_transactions: int = 3,
    window_minutes: int = 60,
    amount_tolerance: float = 0.10,
) -> pd.DataFrame:
    """Flag repeated similar-value transactions to different recipients."""

    df = transactions.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df = df.sort_values(
        ["sender_id", "timestamp"]
    ).reset_index(drop=True)

    df["structuring_flag"] = False

    for sender_id, group in df.groupby("sender_id"):
        group = group.sort_values("timestamp")

        for index, row in group.iterrows():
            window_start = (
                row["timestamp"]
                - pd.Timedelta(minutes=window_minutes)
            )

            window = group[
                (group["timestamp"] >= window_start)
                & (group["timestamp"] <= row["timestamp"])
            ]

            if len(window) < min_transactions:
                continue

            unique_recipients = window["receiver_id"].nunique()

            if unique_recipients < min_transactions:
                continue

            mean_amount = window["amount"].mean()

            if mean_amount == 0:
                continue

            amount_difference = (
                (window["amount"] - mean_amount).abs()
                / mean_amount
            )

            similar_amounts = (
                amount_difference <= amount_tolerance
            ).sum()

            if similar_amounts >= min_transactions:
                df.loc[
                    window.index,
                    "structuring_flag",
                ] = True

    return df