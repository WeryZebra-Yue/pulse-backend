from typing import List, Optional, Union
from beanie import PydanticObjectId
from models.charity import Charity


async def add_charity(new_charity: Charity) -> Charity:
    charity = await new_charity.create()
    return charity


async def retrieve_charities() -> List[Charity]:
    charities = await Charity.all().to_list()
    return charities


async def retrieve_charities_by_alert(alert_id: str) -> List[Charity]:
    charities = await Charity.find(Charity.alert_id == alert_id).to_list()
    return charities


async def retrieve_charity(id: PydanticObjectId) -> Optional[Charity]:
    charity = await Charity.get(id)
    return charity


async def update_charity(id: PydanticObjectId, data: dict) -> Union[Charity, bool]:
    charity = await Charity.get(id)
    if not charity:
        return False
    update_data = {k: v for k, v in data.items() if v is not None}
    await charity.update({"$set": update_data})
    return charity


async def delete_charity(id: PydanticObjectId) -> bool:
    charity = await Charity.get(id)
    if not charity:
        return False
    await charity.delete()
    return True
