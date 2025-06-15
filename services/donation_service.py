from typing import List, Union, Optional
from beanie import PydanticObjectId
from models.donation import Donation


async def add_donation(new_donation: Donation) -> Donation:
    donation = await new_donation.create()
    return donation


async def retrieve_donations() -> List[Donation]:
    donations = await Donation.all().to_list()
    return donations

async def retrieve_donations_by_user(user_id: PydanticObjectId) -> List[Donation]:
    donations = await Donation.find(Donation.user_id == user_id).to_list()
    return donations

async def retrieve_donation(id: PydanticObjectId) -> Optional[Donation]:
    donation = await Donation.get(id)
    return donation


async def update_donation(id: PydanticObjectId, data: dict) -> Union[Donation, bool]:
    donation = await Donation.get(id)
    if not donation:
        return False
    update_data = {k: v for k, v in data.items() if v is not None}
    await donation.update({"$set": update_data})
    return donation


async def delete_donation(id: PydanticObjectId) -> bool:
    donation = await Donation.get(id)
    if not donation:
        return False
    await donation.delete()
    return True
    