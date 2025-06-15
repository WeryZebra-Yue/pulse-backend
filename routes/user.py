from fastapi import APIRouter, Body
from beanie import PydanticObjectId
from typing import List

from models.user import User
from schemas.user import UserResponse, UpdateUserModel
from services.user_service import (
    add_user,
    retrieve_users,
    retrieve_user,
    update_user_data,
    delete_user,
)

router = APIRouter()


@router.get(
    "/", 
    
    description="Retrieve a count of all active users registered on the AidAgent platform. Returns the total number of unique user accounts created, which is essential for platform analytics, user engagement metrics, and monitoring community growth. Useful for administrative dashboards, user base statistics, and evaluating platform reach. Does not return individual user data for privacy reasons."
)
async def get_users():
    active_users = await User.find().count()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Active users retrieved successfully",
        "active_users": active_users,
    }

@router.get(
    "/{id}", 
    response_model=UserResponse,
    description="Retrieve detailed information for a specific user by their unique MongoDB ObjectId. Returns complete user profile including fullname, email, wallet address, registration timestamp, and optional location data. Essential for user profile management, authentication verification, and personalized user experiences. Returns 404 if user not found."
)
async def get_user(id: PydanticObjectId):
    user = await retrieve_user(id)
    if user:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "User retrieved successfully",
            "data": user,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "User not found",
        "data": None,
    }


@router.post(
    "/", 
    response_model=UserResponse,
    description="Create a new user account in the AidAgent platform with wallet-based identity. Requires fullname, email, and wallet_address as mandatory fields. The wallet_address serves as the primary identity mechanism for blockchain-based donations and transactions. Optional location field can store GPS coordinates or text-based location. Automatically timestamps registration with UTC datetime. Returns 201 status with created user data."
)
async def create_user(user: User = Body(...)):
    new_user = await add_user(user)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "User created successfully",
        "data": new_user,
    }


@router.put(
    "/{id}", 
    response_model=UserResponse,
    description="Update existing user account information by MongoDB ObjectId. Supports partial updates through UpdateUserModel schema - only provided fields will be modified while preserving existing data. Commonly used for profile updates, location changes, or contact information modifications. Maintains data integrity by validating email format and preserving wallet address immutability. Returns 404 if user not found."
)
async def update_user(id: PydanticObjectId, req: UpdateUserModel = Body(...)):
    updated_user = await update_user_data(id, req.dict())
    if updated_user:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "User updated successfully",
            "data": updated_user,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "User not found",
        "data": None,
    }


@router.delete(
    "/{id}", 
    response_model=UserResponse,
    description="Permanently delete a user account from the AidAgent platform by MongoDB ObjectId. This is a destructive operation that removes all user data including profile information, registration history, and associated metadata. Use with caution as this action is irreversible. Consider implementing soft delete or account deactivation for production environments. Returns confirmation with deleted user ID or 404 if user not found."
)
async def delete_user_route(id: PydanticObjectId):
    deleted = await delete_user(id)
    if deleted:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"User with ID {id} deleted successfully",
            "data": True,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "User not found",
        "data": False,
    }
from datetime import datetime, timedelta
