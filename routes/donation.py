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
    retrieve_donations_history,
    retrieve_donations_done_by_user
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
    "/transaction", 
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

# total donations amount done by a user
@router.get(
    "/total/{user_id}", 
    response_model=Response,
    description="Calculate the total amount of cryptocurrency donations made by a specific user identified by their wallet address. Aggregates all donation records associated with the provided user_id, summing up the donation amounts across all transactions. Essential for donor recognition, financial reporting, and tracking individual donor contributions to charitable causes. Returns 404 if no donations found for the user."
)
async def get_total_donations_amount_by_user(user_id: PydanticObjectId):
    donations, donation_amount = await retrieve_donations_done_by_user(user_id)
    if donations:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Total donations retrieved successfully",
            "data": {
                "donations": donations,
                "total_amount": donation_amount
            },
        }
    raise HTTPException(status_code=404, detail="No donations found for the user")

# get history of donations done by a user
@router.get(
    "/history/{user_id}", 
    response_model=Response,
    description="Retrieve the complete history of cryptocurrency donations made by a specific user identified by their wallet address. Returns all donation records associated with the provided user_id, including amounts, currencies, timestamps, and linked charities. Essential for donor transparency, financial tracking, and generating personalized donor reports. Returns 404 if no donation history found for the user."
)
async def retrieve_donations_history_by_user(user_id: PydanticObjectId):
    donations = await retrieve_donations_history(user_id)
    if donations:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Donations history retrieved successfully",
            "data": donations,
        }
    raise HTTPException(status_code=404, detail="No donation history found for the user")
