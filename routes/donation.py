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


@router.get(
    "/", 
    response_model=Response,
    description="Retrieve a comprehensive list of all cryptocurrency donations made through the AidAgent platform. Returns complete donation records including donor wallet addresses, donation amounts, currency types (ETH, BTC, USDC, etc.), transaction timestamps, and associated charity identifiers. Essential for financial transparency, donation tracking, audit trails, and generating donation reports. Supports administrative oversight, tax reporting, and donor recognition programs."
)
async def get_donations():
    donations = await retrieve_donations()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Donations retrieved successfully",
        "data": donations,
    }


@router.get(
    "/{id}", 
    response_model=Response,
    description="Retrieve detailed information for a specific cryptocurrency donation by its unique MongoDB ObjectId. Returns complete donation record including donor wallet address, exact donation amount, cryptocurrency type, transaction timestamp, and linked charity identifier. Critical for donation verification, transaction auditing, dispute resolution, and providing donors with detailed contribution receipts. Returns 404 if donation record not found."
)
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


@router.post(
    "/", 
    response_model=Response,
    description="Record a new cryptocurrency donation transaction in the AidAgent platform. Requires donor_wallet (blockchain address), amount (numeric value), currency (ETH, BTC, USDC, etc.), and charity_id as mandatory fields. Automatically timestamps the donation with UTC datetime for accurate record-keeping. Essential for tracking blockchain-based charitable contributions, maintaining donation transparency, and linking contributions to specific charitable organizations. Returns 201 status with created donation record."
)
async def create_donation(donation: Donation = Body(...)):
    new_donation = await add_donation(donation)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Donation created successfully",
        "data": new_donation,
    }


@router.put(
    "/{id}", 
    response_model=Response,
    description="Update existing cryptocurrency donation record by MongoDB ObjectId. Supports partial updates through UpdateDonationModel schema - only provided fields will be modified while preserving existing donation data. Commonly used for correcting transaction details, updating charity associations, or adding additional metadata. Use with caution as donation records should generally be immutable for audit integrity. Maintains financial record accuracy while allowing necessary corrections. Returns 404 if donation not found."
)
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


@router.delete(
    "/{id}", 
    response_model=Response,
    description="Permanently delete a cryptocurrency donation record from the AidAgent platform by MongoDB ObjectId. This is a destructive operation that removes all donation data including wallet addresses, amounts, currency information, timestamps, and charity associations. Use with extreme caution as this action is irreversible and may violate financial audit requirements. Consider implementing donation record archival or soft deletion for production environments to maintain regulatory compliance and audit trails."
)
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
