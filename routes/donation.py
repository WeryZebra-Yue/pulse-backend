from fastapi import APIRouter, Body, HTTPException
from beanie import PydanticObjectId
from typing import List
from models.donation import Donation
from schemas.donation import Response, DonationModel, UpdateDonationModel
from services.donation_service import (
    add_donation,
    retrieve_donations,
    retrieve_donation,
    update_donation,
    delete_donation,
)

router = APIRouter()


@router.get("/", response_model=Response)
async def get_donations():
    donations = await retrieve_donations()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Donations retrieved successfully",
        "data": donations,
    }


@router.get("/{id}", response_model=Response)
async def get_donation(id: PydanticObjectId):
    donation = await retrieve_donation(id)
    if donation:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Donation retrieved successfully",
            "data": donation,
        }
    raise HTTPException(status_code=404, detail="Donation not found")


@router.post("/", response_model=Response)
async def create_donation(donation: Donation = Body(...)):
    new_donation = await add_donation(donation)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Donation created successfully",
        "data": new_donation,
    }


@router.put("/{id}", response_model=Response)
async def update_donation_route(id: PydanticObjectId, req: UpdateDonationModel = Body(...)):
    updated_donation = await update_donation(id, req.dict())
    if updated_donation:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Donation updated successfully",
            "data": updated_donation,
        }
    raise HTTPException(status_code=404, detail="Donation not found")


@router.delete("/{id}", response_model=Response)
async def delete_donation_route(id: PydanticObjectId):
    deleted = await delete_donation(id)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Donation with ID {id} deleted successfully",
            "data": True,
        }
    raise HTTPException(status_code=404, detail="Donation not found")
