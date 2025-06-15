from typing import List, Union
from beanie import PydanticObjectId
from models.user import User


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user


async def retrieve_users() -> List[User]:
    users = await User.all().to_list()
    return users


async def retrieve_user(id: PydanticObjectId) -> Union[User, None]:
    user = await User.get(id)
    return user


async def update_user_data(id: PydanticObjectId, data: dict) -> Union[User, bool]:
    user = await User.get(id)
    if not user:
        return False
    update_data = {k: v for k, v in data.items() if v is not None}
    await user.update({"$set": update_data})
    return user


async def delete_user(id: PydanticObjectId) -> bool:
    user = await User.get(id)
    if not user:
        return False
    await user.delete()
    return True
