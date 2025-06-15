from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime


class Donation(Document):
    donor_wallet: str
    amount: float
    currency: str  # e.g., ETH, BTC, USDC
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    charity_id: str  # Link to related charity

    class Settings:
        name = "donations"
