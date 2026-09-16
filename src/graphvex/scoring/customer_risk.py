import pandas as pd


def calculate_customer_risk(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate transaction-level AML signals into customer-level risk."""

    df = transactions.copy()

    # --------------------------------------------------
    # Sender activity
    # --------------------------------------------------

    sender = (
        df.groupby("sender_id")
        .agg(
            transactions_sent=("transaction_id", "count"),
            total_sent=("amount", "sum"),
            high_velocity_alerts=("high_velocity_flag", "sum"),
            unusual_amount_alerts=("unusual_amount_flag", "sum"),
            structuring_alerts=("structuring_flag", "sum"),
            circular_flow_alerts=("circular_flow_flag", "sum"),
        )
        .rename_axis("customer_id")
    )

    # --------------------------------------------------
    # Receiver activity
    # --------------------------------------------------

    receiver = (
        df.groupby("receiver_id")
        .agg(
            transactions_received=("transaction_id", "count"),
            total_received=("amount", "sum"),
        )
        .rename_axis("customer_id")
    )

    # --------------------------------------------------
    # Combine activity
    # --------------------------------------------------

    customer_risk = sender.join(
        receiver,
        how="outer",
    ).fillna(0)

    # --------------------------------------------------
    # Total alert count
    # --------------------------------------------------

    customer_risk["total_alerts"] = (
        customer_risk["high_velocity_alerts"]
        + customer_risk["unusual_amount_alerts"]
        + customer_risk["structuring_alerts"]
        + customer_risk["circular_flow_alerts"]
    )

    # --------------------------------------------------
    # Customer risk score
    #
    # Each signal type contributes at most once.
    # Repeated alerts are retained as context but
    # do not endlessly inflate the risk score.
    # --------------------------------------------------

    customer_risk["customer_risk_score"] = (
        (customer_risk["high_velocity_alerts"] > 0) * 20
        + (customer_risk["unusual_amount_alerts"] > 0) * 30
        + (customer_risk["structuring_alerts"] > 0) * 25
        + (customer_risk["circular_flow_alerts"] > 0) * 40
    )

    # --------------------------------------------------
    # Risk level
    # --------------------------------------------------

    customer_risk["risk_level"] = pd.cut(
        customer_risk["customer_risk_score"],
        bins=[-1, 0, 30, 60, float("inf")],
        labels=[
            "low",
            "medium",
            "high",
            "critical",
        ],
    )

    return customer_risk.reset_index()