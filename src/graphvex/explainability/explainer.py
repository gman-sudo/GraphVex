import pandas as pd


def generate_explanation(
    transaction: pd.Series,
) -> str:
    """Generate a human-readable explanation for a transaction."""

    reasons = []

    if transaction["high_velocity_flag"]:
        reasons.append(
            "High transaction velocity"
        )

    if transaction["unusual_amount_flag"]:
        reasons.append(
            "Transaction amount is unusual "
            "relative to the sender's historical behaviour"
        )

    if transaction["structuring_flag"]:
        reasons.append(
            "Structuring-like transaction pattern"
        )

    if transaction["circular_flow_flag"]:
        reasons.append(
            "Transaction participates in a circular "
            "fund flow"
        )

    if not reasons:
        return "No significant AML risk signals detected."

    return "; ".join(reasons)