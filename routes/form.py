from fastapi import APIRouter, Body, HTTPException
from typing import Optional
from models.form import Form
from schemas.form import FormModel, NewMessageModel, Response
from services.form_service import get_form_by_alert, add_message_to_form
from services.form_service import get_active_form_by_user

router = APIRouter()


@router.get(
    "/alert/{alert_id}", 
    response_model=Response,
    description="Retrieve the communication form associated with a specific emergency alert by alert_id. Returns the complete form structure including all message threads, user communications, timestamps, and form metadata. Each form contains an array of messages with user_id (wallet address or user identifier), message content, and UTC timestamps. Essential for emergency communication coordination, stakeholder updates, and maintaining communication audit trails during crisis response. Returns 404 if no form exists for the specified alert."
)
async def get_form(alert_id: str):
    form = await get_form_by_alert(alert_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found for this alert")
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Form retrieved successfully",
        "data": form,
    }


@router.post(
    "/alert/{alert_id}/message", 
    response_model=Response,
    description="Add a new message to the communication form associated with a specific emergency alert. Requires user_id (wallet address or user identifier) and message content through NewMessageModel schema. Automatically timestamps the message with UTC datetime and appends it to the existing message thread. Updates the form's last modified timestamp for tracking communication activity. Critical for real-time emergency communication, stakeholder coordination, status updates, and maintaining chronological communication records during crisis response efforts."
)
async def post_message(alert_id: str, message: NewMessageModel = Body(...)):
    form = await add_message_to_form(alert_id, message.dict())
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Message added to form",
        "data": form,
    }


@router.post(
    "/user/{user_id}/active_alerts_forum",
    response_model=Response,
    description="Retrieve a list of active communities for a specific user based on their user_id. Returns an array of community identifiers where the user is actively participating. Useful for personalized user experiences, community engagement tracking, and facilitating targeted communications within active community groups."
)
async def get_active_alerts_by_user(user_id: str):
    """
    This endpoint retrieves the active communities for a user based on their user_id.
    It returns a list of community identifiers where the user is actively participating.
    """
    forums = await get_active_form_by_user(user_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Active communities retrieved successfully",
        "data": forums,
    }