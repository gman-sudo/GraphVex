from datetime import timedelta
from decimal import Decimal

from graphvex.ingestion.schema import Transaction


def generate_structuring_scenario(
    sender_id: str,
    receiver_ids: list[str],
    start_time,
) -> list[Transaction]:
    """Generate a synthetic structuring pattern."""

    amounts = [
        Decimal("9800.00"),
        Decimal("9700.00"),
        Decimal("9900.00"),
        Decimal("9600.00"),
    ]

    transactions = []

    for index, (receiver_id, amount) in enumerate(
        zip(receiver_ids, amounts),
        start=1,
    ):
        transactions.append(
            Transaction(
                transaction_id=f"STRUCT{index:04d}",
                timestamp=start_time + timedelta(minutes=index * 5),
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                currency="AED",
                transaction_type="transfer",
                channel="bank_transfer",
                sender_country="AE",
                receiver_country="AE",
            )
        )

    return transactions

def generate_rapid_movement_scenario(
    account_ids: list[str],
    start_time,
) -> list[Transaction]:
    """Generate a synthetic rapid movement pattern."""

    amounts = [
        Decimal("50000.00"),
        Decimal("49500.00"),
        Decimal("48900.00"),
    ]

    transactions = []

    for index, amount in enumerate(amounts):
        transactions.append(
            Transaction(
                transaction_id=f"RAPID{index + 1:04d}",
                timestamp=start_time + timedelta(minutes=index * 4),
                sender_id=account_ids[index],
                receiver_id=account_ids[index + 1],
                amount=amount,
                currency="AED",
                transaction_type="transfer",
                channel="bank_transfer",
                sender_country="AE",
                receiver_country="AE",
            )
        )

    return transactions


def generate_circular_flow_scenario(
    account_ids: list[str],
    start_time,
) -> list[Transaction]:
    """Generate a synthetic circular flow pattern."""

    amount = Decimal("10000.00")

    transactions = []

    for index in range(len(account_ids)):
        sender_id = account_ids[index]
        receiver_id = account_ids[
            (index + 1) % len(account_ids)
        ]

        transactions.append(
            Transaction(
                transaction_id=f"CIRC{index + 1:04d}",
                timestamp=start_time + timedelta(
                    minutes=index * 10
                ),
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount - Decimal(index * 100),
                currency="AED",
                transaction_type="transfer",
                channel="bank_transfer",
                sender_country="AE",
                receiver_country="AE",
            )
        )

    return transactions

def generate_network_dispersion_scenario(
    sender_id: str,
    receiver_ids: list[str],
    start_time,
) -> list[Transaction]:
    """Generate a synthetic network dispersion pattern."""

    transactions = []

    for index, receiver_id in enumerate(receiver_ids):
        amount = Decimal("5000.00") - Decimal(index * 250)

        transactions.append(
            Transaction(
                transaction_id=f"DISP{index + 1:04d}",
                timestamp=start_time + timedelta(
                    minutes=index * 6
                ),
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount=amount,
                currency="AED",
                transaction_type="transfer",
                channel="bank_transfer",
                sender_country="AE",
                receiver_country="AE",
            )
        )

    return transactions