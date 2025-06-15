import google.generativeai as genai
from models.alert_chat import AlertChat
from config.config import Settings
from typing import List, Dict
from datetime import datetime
from models.alert import Alert

genai.configure(api_key=Settings().genai_api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")


async def chat_about_alert(alert_id: str, user_message: str, user_id: str) -> str:
    # Find or create chat session
    alert_chat = await AlertChat.find_one(
        AlertChat.alert_id == alert_id, AlertChat.user_id == user_id
    )
    alert = await Alert.find_one(Alert.alert_id == alert_id)
    alert_context ={
            "alert_id": alert.alert_id,
            "message": alert.message,
            "location": alert.location,
            "city": alert.city,
            "related_request_id": alert.related_request_id,
            "timestamp": alert.timestamp.isoformat(),
            "aid_available": alert.aid_available,
            "missing_persons_reported": alert.missing_persons_reported,
            "source": alert.source,
            "details": alert.details
        }
    if not alert_chat:
        alert_chat = AlertChat(alert_id=alert_id, user_id=user_id, messages=[])
        await alert_chat.create()

    # Add user message to conversation history
    alert_chat.messages.append({
        "role": "user",
        "content": user_message ,
        "timestamp": datetime.utcnow(),
    })

    # Prepare recent messages (limit to last 5)
    recent_messages = alert_chat.messages[-5:]

    # Convert to Gemini-compatible format
    prompt = [
        {
            "role": "assistant",
            "parts": [
                f"You are a helpful assistant that provides information about alerts. You will answer questions based on the alert details provided. Nothing else. | Context: {alert_context}. You are a helpful assistant that provides information about alerts. You will answer questions based on the alert details provided. Nothing else."
            ]
        }
    ]
    prompt.extend([
        {
            "role": "model" if msg["role"] == "ai" else msg["role"],
            "parts": [
                f'{msg["content"]}'
            ]
        }
        for msg in recent_messages
    ])

    # Get Gemini response
    try:
        gemini_response = await ask_gemini_with_context(prompt)
    except Exception as e:
        return f"Failed to get response from Gemini: {e}"

    # Save AI response
    alert_chat.messages.append({
        "role": "ai",
        "content": gemini_response,
        "timestamp": datetime.utcnow()
    })

    await alert_chat.save()
    return gemini_response


async def ask_gemini_with_context(prompt: List[Dict[str, str]]) -> str:
    """
    Send properly formatted message history to Gemini and return AI response.
    Each message must follow Gemini's expected format.
    """
    try:
        # Start chat with full history
        chat = model.start_chat(history=prompt)

        # Get last user message for reply
        last_user_message = next(
            m["parts"][0] for m in reversed(prompt) if m["role"] == "user"
        )

        # Send message and return response
        response = chat.send_message(last_user_message)
        return response.text.strip()
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return "Sorry, I couldn't process your request at the moment."

async def get_chat_history(alert_id: str, user_id: str) -> List[Dict[str, str]]:
    """
    Retrieve chat history for a specific alert and user.
    Returns a list of messages with roles and content.
    """
    alert_chat = await AlertChat.find_one(
        AlertChat.alert_id == alert_id, AlertChat.user_id == user_id
    )
    
    if not alert_chat:
        return []

    # Format messages for output
    chat_history = [
        {
            "role": msg["role"],
            "content": msg["content"],
            "timestamp": msg["timestamp"].isoformat()
        }
        for msg in alert_chat.messages
    ]
    
    return chat_history