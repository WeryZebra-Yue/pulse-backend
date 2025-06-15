from typing import Optional, Any
from pydantic import BaseModel


class DonationModel(BaseModel):
    donor_wallet: str
    amount: float
    currency: str
    related_request_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "donor_wallet": "0x123abc456def789",
                "amount": 100.0,
                "currency": "ETH",
                "related_request_id": "req123",
            }
        }


class UpdateDonationModel(BaseModel):
    amount: Optional[float]
    currency: Optional[str]
    related_request_id: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 120.0,
                "currency": "USDC",
                "related_request_id": "req456",
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]
