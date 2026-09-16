from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    """Canonical GraphVex transaction model."""

    transaction_id: str = Field(min_length=1)
    timestamp: datetime

    sender_id: str = Field(min_length=1)
    receiver_id: str = Field(min_length=1)

    amount: Decimal = Field(gt=0)
    currency: str = Field(
    min_length=3,
    max_length=3,
    pattern=r"^[A-Z]{3}$",
    )

    transaction_type: str | None = None
    channel: str | None = None

    sender_country: str | None = None
    receiver_country: str | None = None