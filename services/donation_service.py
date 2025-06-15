from typing import List, Union, Optional
from beanie import PydanticObjectId
from models.donation import Donation
from solana.rpc.async_api import AsyncClient

async def verify_transaction(tx_signature: str) -> bool:
    client = AsyncClient("https://api.mainnet-beta.solana.com")
    resp = await client.get_confirmed_transaction(tx_signature)
    await client.close()

    # If transaction exists and confirmed, return True else False
    return resp['result'] is not None


async def add_donation(new_donation: Donation) -> Donation:
    # donation = await new_donation.create()
    tx_signature = new_donation.tx_signature
    # is_verified = await verify_transaction(tx_signature)
    # if not is_verified:
    #     raise ValueError("Transaction verification failed. Please check the transaction signature.")
    donation = await new_donation.create()
    if not donation:
        raise ValueError("Failed to create donation record.")
    # Optionally, you can update the status of the donation based on verification
    donation.status = "confirmed"
    await donation.save()
    # Return the created donation object
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
    
async def retrieve_donations_done_by_user(user_id: PydanticObjectId) -> List[Donation]:
    """
    Retrieve all donations made by a specific user.
    """
    donations = await Donation.find(Donation.user_id == user_id).to_list()
    donation_amount = sum(donation.amount for donation in donations)
    return donations, donation_amount
