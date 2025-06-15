from pydantic import BaseModel, Field
from typing import Optional, Any


class CharityModel(BaseModel):
    charity_id: str = Field(..., example="charity123")
    name: str = Field(..., example="Helping Hands")
    description: Optional[str] = Field(None, example="A charity organization helping those in need.")
    location: Optional[str] = Field(None, example="Berlin, Germany")
    contact_info: Optional[str] = Field(None, example="+49 123 4567890")
    website: Optional[str] = Field(None, example="https://www.helpinghands.org")
    alert_id: str = Field(..., example="alert123")

    class Config:
        json_schema_extra = {
            "example": {
                "charity_id": "charity123",
                "name": "Helping Hands",
                "description": "A charity organization helping those in need.",
                "location": "Berlin, Germany",
                "contact_info": "+49 123 4567890",
                "website": "https://www.helpinghands.org",
                "alert_id": "alert123",
            }
        }


class UpdateCharityModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    location: Optional[str]
    contact_info: Optional[str]
    website: Optional[str]
    alert_id: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Helping Hands Updated",
                "description": "Updated description",
                "location": "Munich, Germany",
                "contact_info": "+49 987 654321",
                "website": "https://updated.org",
                "alert_id": "alert456",
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]
