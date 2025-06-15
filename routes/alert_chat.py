from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from models.alert_chat import AlertChat
from services.alert_chat_service import chat_about_alert

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    alert_id: str
    user_id: str = Body(..., description="ID of the user sending the message")

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await chat_about_alert(request.alert_id, request.message, request.user_id)
    if not reply:
        raise HTTPException(status_code=500, detail="AI response error")
    return ChatResponse(reply=reply)

@router.get("/chat/{alert_id}", response_model=AlertChat)
async def get_chat_history(alert_id: str, user_id: str):
    """
    Retrieve chat history for a specific alert and user.
    Returns the AlertChat document containing all messages.
    """
    chat_history = await AlertChat.find_one(
        AlertChat.alert_id == alert_id, AlertChat.user_id == user_id
    )
    
    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    
    return chat_history
