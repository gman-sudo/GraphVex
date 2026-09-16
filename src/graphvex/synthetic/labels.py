from dataclasses import dataclass


@dataclass(frozen=True)
class GroundTruthLabel:
    """Evaluation label for a synthetic transaction."""

    transaction_id: str
    scenario: str

def label_normal_transactions(
    transaction_ids: list[str],
) -> list[GroundTruthLabel]:
    """Label transactions that belong to normal activity."""

    return [
        GroundTruthLabel(
            transaction_id=transaction_id,
            scenario="normal",
        )
        for transaction_id in transaction_ids
    ]

def label_scenario_transactions(
    transaction_ids: list[str],
    scenario: str,
) -> list[GroundTruthLabel]:
    """Label transactions belonging to a known scenario."""

    return [
        GroundTruthLabel(
            transaction_id=transaction_id,
            scenario=scenario,
        )
        for transaction_id in transaction_ids
    ]