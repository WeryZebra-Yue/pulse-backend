from fastapi import APIRouter, Body, HTTPException
from typing import Optional
from models.form import Form
from schemas.form import FormModel, NewMessageModel, Response
from services.form_service import get_form_by_alert, add_message_to_form

router = APIRouter()


@router.get("/alert/{alert_id}", response_model=Response)
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


@router.post("/alert/{alert_id}/message", response_model=Response)
async def post_message(alert_id: str, message: NewMessageModel = Body(...)):
    form = await add_message_to_form(alert_id, message.dict())
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Message added to form",
        "data": form,
    }
