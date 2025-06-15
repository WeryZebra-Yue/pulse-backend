from beanie import Document
from pydantic import Field
from typing import Optional


class Charity(Document):
    name: str
    description: Optional[str]
    location: Optional[str]
    contact_info: Optional[str]
    website: Optional[str]
    alert_id: str  # Link to related alert
    wallet_address: str  # Solana wallet address for donations

    class Settings:
        name = "charities"
