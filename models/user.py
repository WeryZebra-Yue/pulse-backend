from typing import Optional, List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import Dict


class User(Document):
    fullname: str
    email: EmailStr
    wallet_address: str  # Wallet-based identity
    registered_on: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = None  # Could be GPS coordinates or text
    class Settings:
        name = "users"

