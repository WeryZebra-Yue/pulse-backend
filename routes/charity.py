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


@router.get("/", response_model=Response)
async def get_charities():
    charities = await retrieve_charities()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Charities retrieved successfully",
        "data": charities,
    }


@router.get("/alert/{alert_id}", response_model=Response)
async def get_charities_by_alert(alert_id: str):
    charities = await retrieve_charities_by_alert(alert_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"Charities related to alert {alert_id} retrieved successfully",
        "data": charities,
    }


@router.get("/{id}", response_model=Response)
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


@router.post("/", response_model=Response)
async def create_charity(charity: Charity = Body(...)):
    new_charity = await add_charity(charity)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Charity created successfully",
        "data": new_charity,
    }


@router.put("/{id}", response_model=Response)
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


@router.delete("/{id}", response_model=Response)
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
