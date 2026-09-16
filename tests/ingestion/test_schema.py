from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from graphvex.ingestion.schema import Transaction


def test_valid_transaction():
    transaction = Transaction(
        transaction_id="TX001",
        timestamp=datetime(2026, 1, 15, 10, 30, tzinfo=UTC),
        sender_id="C001",
        receiver_id="C002",
        amount=Decimal("5000.00"),
        currency="AED",
    )

    assert transaction.transaction_id == "TX001"
    assert transaction.amount == Decimal("5000.00")
    assert transaction.currency == "AED"


def test_transaction_rejects_negative_amount():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TX002",
            timestamp=datetime(2026, 1, 15, 10, 30, tzinfo=UTC),
            sender_id="C001",
            receiver_id="C002",
            amount=Decimal(-100),
            currency="AED",
        )


def test_transaction_rejects_zero_amount():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TX003",
            timestamp=datetime(2026, 1, 15, 10, 30, tzinfo=UTC),
            sender_id="C001",
            receiver_id="C002",
            amount=Decimal(0),
            currency="AED",
        )


def test_transaction_rejects_empty_transaction_id():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="",
            timestamp=datetime(2026, 1, 15, 10, 30, tzinfo=UTC),
            sender_id="C001",
            receiver_id="C002",
            amount=Decimal(500),
            currency="AED",
        )


def test_transaction_rejects_invalid_currency_length():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TX004",
            timestamp=datetime(2026, 1, 15, 10, 30, tzinfo=UTC),
            sender_id="C001",
            receiver_id="C002",
            amount=Decimal(500),
            currency="US",
        )