from typing import Optional, List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict
# from solana.publickey import PublicKey


class User(Document):
    fullname: str
    email: EmailStr
    wallet_address: str  # Wallet-based identity
    registered_on: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = None  # Could be GPS coordinates or text
    class Settings:
        name = "users"

    # @validator("solana_wallet")
    # def validate_solana_address(cls, v):
    #     if v is None:
    #         return v
    #     try:
    #         PublicKey(v)
    #     except Exception:
    #         raise ValueError("Invalid Solana wallet address")
    #     return v
