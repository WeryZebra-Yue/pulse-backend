from fastapi import APIRouter, Body, HTTPException
from typing import List
from beanie import PydanticObjectId
from models.charity import Charity
from schemas.charity import CharityModel, UpdateCharityModel, Response
from services.charity_service import (
    add_charity,
    retrieve_charities,
    retrieve_charities_by_alert,
    retrieve_charity,
    update_charity,
    delete_charity,
)

router = APIRouter()


@router.get(
    "/", 
    response_model=Response,
    description="Retrieve a comprehensive list of all registered charitable organizations in the AidAgent platform. Returns complete charity profiles including charity_id, organization name, description, geographical location, contact information, website URLs, and associated alert_id linkages. Essential for donors seeking verified charitable organizations, aid coordination efforts, and maintaining a centralized registry of humanitarian organizations. Supports administrative oversight and charity verification processes."
)
async def get_charities():
    charities = await retrieve_charities()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Charities retrieved successfully",
        "data": charities,
    }


@router.get(
    "/alert/{alert_id}", 
    response_model=Response,
    description="Retrieve all charitable organizations specifically associated with a particular emergency alert by alert_id. This endpoint enables targeted charity discovery based on emergency context, allowing donors to find organizations actively responding to specific disasters or crises. Returns filtered charity list with complete organizational details including contact information, location data, and operational focus. Critical for emergency-specific donation routing and coordinated humanitarian response efforts."
)
async def get_charities_by_alert(alert_id: str):
    charities = await retrieve_charities_by_alert(alert_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"Charities related to alert {alert_id} retrieved successfully",
        "data": charities,
    }


@router.get(
    "/{id}", 
    response_model=Response,
    description="Retrieve detailed information for a specific charitable organization by its unique MongoDB ObjectId. Returns comprehensive charity profile including charity_id, organization name, mission description, operational location, contact details, official website, and linked emergency alert context. Essential for due diligence processes, donor verification, detailed charity research, and integration with external charity rating systems. Returns 404 if charity not found."
)
async def get_charity(id: PydanticObjectId):
    charity = await retrieve_charity(id)
    if charity:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Charity retrieved successfully",
            "data": charity,
        }
    raise HTTPException(status_code=404, detail="Charity not found")


@router.post(
    "/", 
    response_model=Response,
    description="Register a new charitable organization in the AidAgent platform. Requires charity_id, name, and alert_id as mandatory fields to establish charity identity and emergency context linkage. Supports optional description for mission statements, location for operational geography, contact_info for communication channels, and website for official online presence. Enables charity onboarding, emergency response registration, and humanitarian organization network expansion. Returns 201 status with created charity data."
)
async def create_charity(charity: Charity = Body(...)):
    new_charity = await add_charity(charity)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Charity created successfully",
        "data": new_charity,
    }


@router.put(
    "/{id}", 
    response_model=Response,
    description="Update existing charitable organization information by MongoDB ObjectId. Supports partial updates through UpdateCharityModel schema - only provided fields will be modified while preserving existing charity data. Commonly used for updating contact information, mission descriptions, operational locations, website URLs, or emergency alert associations. Maintains charity data integrity while allowing organizations to keep their profiles current and accurate. Returns 404 if charity not found."
)
async def update_charity_route(id: PydanticObjectId, req: UpdateCharityModel = Body(...)):
    updated_charity = await update_charity(id, req.dict())
    if updated_charity:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Charity updated successfully",
            "data": updated_charity,
        }
    raise HTTPException(status_code=404, detail="Charity not found")


@router.delete(
    "/{id}", 
    response_model=Response,
    description="Permanently remove a charitable organization from the AidAgent platform by MongoDB ObjectId. This is a destructive operation that deletes all charity data including organizational details, contact information, alert associations, and historical records. Use with extreme caution as this action is irreversible and may impact ongoing donation campaigns and emergency response coordination. Consider implementing charity deactivation or archival processes for production environments to maintain donation audit trails."
)
async def delete_charity_route(id: PydanticObjectId):
    deleted = await delete_charity(id)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Charity with ID {id} deleted successfully",
            "data": True,
        }
    raise HTTPException(status_code=404, detail="Charity not found")
