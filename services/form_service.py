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
