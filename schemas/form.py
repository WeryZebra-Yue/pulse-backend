from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class MessageModel(BaseModel):
    user_id: str = Field(..., example="user123")
    content: str = Field(..., example="Is there any update on the flood relief?")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FormModel(BaseModel):
    alert_id: str = Field(..., example="alert123")
    messages: List[MessageModel]

    class Config:
        orm_mode = True


class NewMessageModel(BaseModel):
    user_id: str = Field(..., example="user123")
    content: str = Field(..., example="Is there any update on the flood relief?")


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: object
