import pandas as pd


RULE_WEIGHTS = {
    "high_velocity_flag": 20,
    "unusual_amount_flag": 30,
    "structuring_flag": 25,
    "circular_flow_flag": 40,
}

def calculate_risk_score(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate a transparent risk score from AML detection signals."""

    df = transactions.copy()

    df["risk_score"] = 0

    for flag, weight in RULE_WEIGHTS.items():
        df["risk_score"] += (
            df[flag].astype(int) * weight
        )

    return df