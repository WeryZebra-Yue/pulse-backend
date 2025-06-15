from typing import Optional
from beanie import PydanticObjectId
from models.form import Form, Message


async def create_form(alert_id: str) -> Form:
    form = Form(alert_id=alert_id)
    await form.create()
    return form


async def get_form_by_alert(alert_id: str) -> Optional[Form]:
    return await Form.find_one(Form.alert_id == alert_id)


async def add_message_to_form(alert_id: str, message_data: dict) -> Optional[Form]:
    form = await get_form_by_alert(alert_id)
    if not form:
        form = await create_form(alert_id)

    message = Message(**message_data)
    await form.add_message(message)
    return form

async def get_active_form_by_user(user_id: PydanticObjectId) -> Optional[Form]:
    """
    Retrieve the active form for a user.
    """
    # write a query to find the form by user_id in any of the messages, message is a list of Message objects
    forms = Form.find({"messages.user_id": user_id}).skip(0).limit(100)
    # return all
    return await forms.to_list() if forms else None 
