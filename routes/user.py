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


@router.get("/", response_model=UserResponse)
async def get_users():
    users = await retrieve_users()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Users retrieved successfully",
        "data": users,
    }


@router.get("/{id}", response_model=UserResponse)
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


@router.post("/", response_model=UserResponse)
async def create_user(user: User = Body(...)):
    new_user = await add_user(user)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "User created successfully",
        "data": new_user,
    }


@router.put("/{id}", response_model=UserResponse)
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


@router.delete("/{id}", response_model=UserResponse)
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
