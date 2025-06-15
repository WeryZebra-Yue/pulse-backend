from beanie import Document
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class Message(BaseModel):
    user_id: str  # Could be wallet address or user ID
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Form(Document):
    alert_id: str  # Link to related alert
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "forms"

    async def add_message(self, message: Message):
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        await self.save()
