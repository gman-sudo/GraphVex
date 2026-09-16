import pandas as pd


def build_investigation_cases(
    customer_risk: pd.DataFrame,
) -> pd.DataFrame:
    """Create investigation cases for customers with AML risk signals."""

    df = customer_risk.copy()

    # --------------------------------------------------
    # Only customers with risk signals
    # --------------------------------------------------

    df = df[
        df["customer_risk_score"] > 0
    ].copy()

    # --------------------------------------------------
    # Build human-readable reasons
    # --------------------------------------------------

    def build_reason(row):
        reasons = []

        if row["high_velocity_alerts"] > 0:
            reasons.append(
                "High transaction velocity"
            )

        if row["unusual_amount_alerts"] > 0:
            reasons.append(
                "Unusual transaction amounts"
            )

        if row["structuring_alerts"] > 0:
            reasons.append(
                "Structuring-like activity"
            )

        if row["circular_flow_alerts"] > 0:
            reasons.append(
                "Circular fund flow"
            )

        return "; ".join(reasons)

    df["reasons"] = df.apply(
        build_reason,
        axis=1,
    )

    # --------------------------------------------------
    # Investigation status
    # --------------------------------------------------

    df["status"] = "open"

    # --------------------------------------------------
    # Select case fields
    # --------------------------------------------------

    cases = df[
        [
            "customer_id",
            "customer_risk_score",
            "risk_level",
            "total_alerts",
            "transactions_sent",
            "transactions_received",
            "reasons",
            "status",
        ]
    ].sort_values(
        "customer_risk_score",
        ascending=False,
    ).reset_index(drop=True)

    # --------------------------------------------------
    # Generate case IDs AFTER sorting by risk
    # --------------------------------------------------

    cases.insert(
        0,
        "case_id",
        [
            f"CASE-{index:04d}"
            for index in range(1, len(cases) + 1)
        ],
    )

    return cases