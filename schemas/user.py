from typing import Optional, Any
from pydantic import BaseModel, EmailStr


class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    wallet_address: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john.doe@example.com",
                "wallet_address": "0x123abc456def789",
            }
        }


class UserResponse(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "User retrieved successfully",
                "data": {
                    "fullname": "John Doe",
                    "email": "john.doe@example.com",
                    "wallet_address": "0x123abc456def789",
                    "registered_on": "2025-06-14T18:00:00Z",
                },
            }
        }
