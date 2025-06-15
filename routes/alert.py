from fastapi import APIRouter, Body, HTTPException
from typing import List
from models.alert import Alert
from schemas.alert import Response, Alert as AlertSchema, UpdateAlertModel
from services.alert_service import (
    add_alert,
    retrieve_alerts,
    retrieve_alert,
    update_alert,
    delete_alert,
    update_alert_if_stale,
)

router = APIRouter()


@router.get("/", response_model=Response)
async def get_alerts(
    location: str = None, refresh: bool = False
):
    alerts = await retrieve_alerts(
        location=location, refresh=refresh
    )
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Alerts retrieved successfully",
        "data": alerts,
    }


@router.get("/{alert_id}", response_model=Response)
async def get_alert(alert_id: str):
    alert = await retrieve_alert(alert_id)
    if alert:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Alert retrieved successfully",
            "data": alert,
        }
    raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/", response_model=Response)
async def create_alert(alert: Alert = Body(...)):
    new_alert = await add_alert(alert)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Alert created successfully",
        "data": new_alert,
    }


@router.put("/{alert_id}", response_model=Response)
async def update_alert_route(alert_id: str, req: UpdateAlertModel = Body(...)):
    updated_alert = await update_alert(alert_id, req.dict())
    if updated_alert:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Alert updated successfully",
            "data": updated_alert,
        }
    raise HTTPException(status_code=404, detail="Alert not found")


@router.delete("/{alert_id}", response_model=Response)
async def delete_alert_route(alert_id: str):
    deleted = await delete_alert(alert_id)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Alert with ID {alert_id} deleted successfully",
            "data": True,
        }
    raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/update_if_stale/{alert_id}", response_model=Response)
async def update_if_stale(alert_id: str):
    alert = await update_alert_if_stale(alert_id)
    if alert:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Alert checked and updated if stale",
            "data": alert,
        }
    raise HTTPException(status_code=404, detail="Alert not found")
