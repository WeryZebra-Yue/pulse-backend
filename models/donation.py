from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional 

class Donation(Document):
    donor_wallet: str  # Solana wallet address
    tx_signature: str  # Transaction signature on Solana
    amount: float
    currency: str  # "SOL" or token name
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, confirmed, failed
    charity_id: Optional[str] = None

    class Settings:
        name = "donations"