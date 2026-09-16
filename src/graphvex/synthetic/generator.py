from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
import random

from graphvex.ingestion.schema import Transaction


@dataclass(frozen=True)
class Customer:
    """Synthetic customer profile."""

    customer_id: str
    country: str
    customer_type: str
    avg_transaction_amount: float
    transactions_per_week: int
    preferred_channel: str


def generate_customers(
    count: int,
    seed: int = 42,
) -> list[Customer]:
    """Generate a reproducible population of synthetic customers."""

    rng = random.Random(seed)

    customers = []

    for index in range(1, count + 1):
        customer_type = rng.choice(
            ["individual", "business"]
        )

        if customer_type == "individual":
            avg_transaction_amount = rng.uniform(300, 3000)
            transactions_per_week = rng.randint(2, 8)
            preferred_channel = rng.choice(
                ["online", "card"]
            )
        else:
            avg_transaction_amount = rng.uniform(5000, 30000)
            transactions_per_week = rng.randint(8, 25)
            preferred_channel = "bank_transfer"

        customers.append(
            Customer(
                customer_id=f"C{index:04d}",
                country="AE",
                customer_type=customer_type,
                avg_transaction_amount=round(
                    avg_transaction_amount, 2
                ),
                transactions_per_week=transactions_per_week,
                preferred_channel=preferred_channel,
            )
        )

    return customers


def generate_transactions(
    customers: list[Customer],
    count: int,
    seed: int = 42,
) -> list[Transaction]:
    """Generate normal synthetic financial transactions."""

    rng = random.Random(seed)

    transactions = []

    start_time = datetime(2026, 1, 1, 0, 0, 0)

    customer_transaction_counts = {}

    for customer in customers:
        expected_count = customer.transactions_per_week * 30 / 7

        variation = rng.uniform(0.8, 1.2)

        transaction_count = max(
            1,
            round(expected_count * variation),
        )

        customer_transaction_counts[customer.customer_id] = (
            transaction_count
        )

    generated_count = 0

    while generated_count < count:
        customer = rng.choice(customers)

        if customer_transaction_counts[customer.customer_id] <= 0:
            continue

        receiver = rng.choice(customers)

        while receiver.customer_id == customer.customer_id:
            receiver = rng.choice(customers)

        amount = (
            customer.avg_transaction_amount
            * rng.uniform(0.5, 1.5)
        )

        timestamp = start_time + timedelta(
            minutes=rng.randint(
                0,
                30 * 24 * 60 - 1,
            )
        )

        transactions.append(
            Transaction(
                transaction_id=f"TX{generated_count + 1:06d}",
                timestamp=timestamp,
                sender_id=customer.customer_id,
                receiver_id=receiver.customer_id,
                amount=Decimal(
                    str(round(amount, 2))
                ),
                currency="AED",
                transaction_type="transfer",
                channel=customer.preferred_channel,
                sender_country=customer.country,
                receiver_country=receiver.country,
            )
        )

        customer_transaction_counts[
            customer.customer_id
        ] -= 1

        generated_count += 1

    return transactions