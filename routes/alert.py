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


@router.get(
    "/", 
    response_model=Response,
    description="Retrieve emergency alerts with optional location-based filtering and refresh capabilities. Supports location parameter for geographically relevant alerts and refresh parameter to force data reload from external sources. Returns comprehensive alert data including alert_id, message content, location coordinates, timestamps, metadata, available aid information, missing persons reports, and source attribution. Essential for emergency response coordination and situational awareness."
)
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


@router.get(
    "/{alert_id}", 
    response_model=Response,
    description="Retrieve detailed information for a specific emergency alert by its unique alert_id. Returns complete alert profile including message content, geographical location, related request identifiers, creation timestamp, metadata, available aid resources, missing persons information, source attribution, and additional contextual details. Critical for emergency response teams, aid coordination, and detailed incident analysis."
)
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


@router.post(
    "/", 
    response_model=Response,
    description="Create a new emergency alert in the AidAgent system. Requires alert_id and message as mandatory fields. Supports optional location (city, country format), related_request_id for linking to external systems, metadata for additional context, aid_available array for resource information, missing_persons_reported for casualty data, source attribution, and details array for comprehensive incident information. Automatically timestamps with UTC datetime. Returns 201 status with created alert data."
)
async def create_alert(alert: Alert = Body(...)):
    new_alert = await add_alert(alert)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Alert created successfully",
        "data": new_alert,
    }


@router.put(
    "/{alert_id}", 
    response_model=Response,
    description="Update existing emergency alert information by alert_id. Supports partial updates through UpdateAlertModel schema - only provided fields will be modified while preserving existing alert data. Commonly used for status updates, adding new aid information, updating missing persons counts, or appending additional details. Maintains alert integrity while allowing real-time information updates during ongoing emergencies. Returns 404 if alert not found."
)
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


@router.delete(
    "/{alert_id}", 
    response_model=Response,
    description="Permanently delete an emergency alert from the AidAgent system by alert_id. This is a destructive operation that removes all alert data including message content, location information, metadata, aid availability data, and associated details. Use with extreme caution as this action is irreversible and may impact ongoing emergency response efforts. Consider implementing alert archival or status-based deactivation for production environments."
)
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


@router.post(
    "/update_if_stale/{alert_id}", 
    response_model=Response,
    description="Intelligent alert freshness management endpoint that checks if an alert's data has become stale and automatically updates it from external sources if necessary. Implements smart caching logic to balance data freshness with API rate limits. Compares last update timestamps against configurable staleness thresholds and triggers data refresh from authoritative sources when needed. Essential for maintaining accurate emergency information without overwhelming external APIs with unnecessary requests."
)
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
