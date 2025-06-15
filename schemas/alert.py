from typing import Optional, Dict, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MetaInfo(BaseModel):
    last_loaded: Optional[datetime] = Field(default=None, example="2025-06-14T18:00:00Z")


class Alert(BaseModel):
    alert_id: str = Field(..., example="alert123")
    message: str = Field(..., example="Flood warning in your area")
    location: Optional[str] = Field(None, example="Berlin, Germany")
    resources: Optional[Dict[str, List[str]]] = Field(
        None,
        example={
            "food": ["Food Shelter 1", "Food Bank 2"],
            "helplines": ["1234", "5678"],
            "shelters": ["Shelter A", "Shelter B"],
        },
    )
    related_request_id: Optional[str] = Field(None, example="req456")
    timestamp: datetime = Field(..., example="2025-06-14T17:00:00Z")
    meta: Optional[MetaInfo] = None

        # class Config:
        #     orm_mode = True


class UpdateAlertModel(BaseModel):
    message: Optional[str] = Field(None, example="Updated flood warning")
    location: Optional[str] = Field(None, example="Berlin, Germany")
    resources: Optional[Dict[str, List[str]]] = None
    related_request_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "message": "Updated flood warning",
                "location": "Berlin, Germany",
                "resources": {
                    "food": ["New Food Shelter"],
                    "helplines": ["4321"],
                    "shelters": ["New Shelter"],
                },
                "related_request_id": "req789",
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": None,
            }
        }
