from datetime import datetime
from typing import Optional, Dict, List
from beanie import Document
from pydantic import BaseModel, Field

class MetaInfo(Document):
    last_loaded: Optional[datetime] = Field(default=None, example="2025-06-14T18:00:00Z")

    class Settings:
        name = "meta_info"

class Alert(Document):
    alert_id: str
    message: str
    location: Optional[str]  # City, Country
    related_request_id: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    meta: Optional[dict] 
    aid_available: Optional[List[dict]] = Field(default_factory=list)
    missing_persons_reported: Optional[str] = None
    source: Optional[str] = "Unknown"
    details: Optional[List[str]] = Field(default_factory=list)

    class Settings:
        name = "alerts"