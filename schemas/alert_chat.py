from beanie import Document
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class ChatMessage(BaseModel):
    sender: str  # "user" or "ai"
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AlertChat(Document):
    alert_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "alert_chats"

    async def add_message(self, sender: str, message: str):
        self.messages.append(ChatMessage(sender=sender, message=message))
        self.updated_at = datetime.utcnow()
        await self.save()
