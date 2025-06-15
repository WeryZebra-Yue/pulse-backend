from typing import Optional, List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Dict
from solana.rpc.api import Pubkey

class User(Document):
    fullname: str
    email: EmailStr
    wallet_address: str  # Wallet-based identity
    registered_on: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = None  # Could be GPS coordinates or text
    class Settings:
        name = "users"

    # @field_validator("wallet_address")
    # def validate_solana_address(cls, v):
    #     if v is None:
    #         return v
    #     try:
    #         Pubkey(v)
    #     except Exception:
    #         raise ValueError("Invalid Solana wallet address")
    #     return v
