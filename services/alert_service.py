import os
import json
import google.generativeai as genai
from typing import List, Union, Optional
from datetime import datetime, timedelta
from beanie import PydanticObjectId
from models.alert import Alert, MetaInfo

async def add_alert(new_alert: Alert) -> Alert:
    alert = await new_alert.create()
    return alert

async def retrieve_alerts(
        location: Optional[str] = None,
        refresh: bool = False
) -> List[Alert]:
    alerts = await Alert.all().to_list()

    should_reload = False
    meta_info = None
    if not alerts:
        should_reload = True
    else:
        # Assuming meta info is stored in one of the alerts, or globally
        meta_info = await MetaInfo.find_one()  # Adjust based on your DB design
        if not meta_info or not meta_info.last_loaded or meta_info.last_loaded < datetime.utcnow() - timedelta(days=1):
            should_reload = True
    if location !="global" or refresh:
        should_reload = True  # Force reload if location is specified
    if should_reload:
        new_data = await fetch_alert_details_from_gemini(location or "global")
        if new_data:
            # Clear old alerts (if needed)
            await Alert.delete_all()
            # Save new alerts
            for alert_dict in new_data :
                print(f"Processing alert: {alert_dict}")
                alert = Alert(
                    alert_id=alert_dict.get("alert_id", str(PydanticObjectId())),
                    message=alert_dict.get("message", ""),
                    location=alert_dict.get("location"),
                    related_request_id=alert_dict.get("related_request_id"),
                    timestamp=alert_dict.get("timestamp", datetime.utcnow()),
                    details=alert_dict.get("details", []),
                    aid_available=alert_dict.get("aid_available", []),
                    missing_persons_reported=alert_dict.get("missing_persons_reported", ""),
                    source=alert_dict.get("source", "Unknown"),
                    meta={  }
                )
                await alert.create()
            # Update meta info
            if meta_info is not None:
                meta_info.last_loaded = datetime.utcnow()
                await meta_info.save()
            else:
                await MetaInfo(last_loaded=datetime.utcnow()).create()
            alerts = await Alert.all().to_list()

    
    return alerts


async def retrieve_alert(alert_id: str) -> Optional[Alert]:
    alert = await Alert.find_one(Alert.alert_id == alert_id)
    return alert


async def update_alert(alert_id: str, data: dict) -> Union[Alert, bool]:
    alert = await Alert.find_one(Alert.alert_id == alert_id)
    if not alert:
        return False
    update_data = {k: v for k, v in data.items() if v is not None}
    await alert.update({"$set": update_data})
    return alert


async def delete_alert(alert_id: str) -> bool:
    alert = await Alert.find_one(Alert.alert_id == alert_id)
    if not alert:
        return False
    await alert.delete()
    return True


# Initialize Gemini
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Create a generative model
model = genai.GenerativeModel("gemini-2.5-flash")

async def fetch_alert_details_from_gemini(location: str = "global") -> Optional[List[dict]]:
    prompt = f"""
    You are AidAgent, an AI system responsible for gathering and organizing crisis-related information.

    Task:
    Fetch the latest data related to disasters in "{location}" (e.g., floods, earthquakes, wildfires, conflicts, pandemics, disaster, crashes) from reliable public sources such as:
    - Government alerts
    - International relief organizations (e.g., UN, Red Cross, WHO)
    - Updates from social medias (e.g., Twitter, public APIs, RSS feeds) (Day one old data is fine.)
    {
      "Include only 3-4 events." if location!="global" else ""
    }
    For each crisis event, extract the following:

    - type: Type of crisis (e.g., Earthquake, Flood)
    - location: Country and region affected
    - timestamp: Date and time of the event or last update (ISO format)
    - source: Verified source of information
    - details: An array of short, factual statements describing the event
    - aid_available: List of support options including:
      - type: e.g., food, shelter, medical, evacuation, counseling
      - location_detail: Where the aid is being provided (specific address or area)
      - helpline_number: If available, include an official contact number
    - missing_persons_reported: Estimated or confirmed number (if available) in string

    Format the output as a JSON array of such event objects.
    Only output valid JSON.
    It does not need to be real-time data, but it should be the most recent information available.
    just return data, without any additional text or explanation.
    Example output:
    [
        {{
            "type": "Flood",
            "location": "Berlin, Germany",
            "timestamp": "2025-06-14T17:00:00Z",
            "source": "Local Government",
            "details": ["Heavy rainfall caused flooding in several districts.", "Emergency services are on alert."],
            "aid_available": [
                {{
                    "type": "food",
                    "location_detail": "Food Shelter 1, Berlin",
                    "helpline_number": "1234"
                }},
                {{
                    "type": "shelter",
                    "location_detail": "Shelter A, Berlin",
                    "helpline_number": "None"
                }}
            ],
            "missing_persons_reported": "5 missing persons reported",
        }}
    ]
    Ensure the output is a valid JSON array of objects, each containing the fields mentioned above.
    Do not include any additional text or explanations, just return the JSON data.
    Sort the events by timestamp in descending order, so the most recent event comes first.
    """

    try:
        response = model.generate_content(prompt)
        print(f"Response from Gemini: {response }")
        json_response = response.text.strip().replace("```json", "").replace("```", "")
        alert_list = json.loads(json_response)
        return alert_list if isinstance(alert_list, list) else []
    except Exception as e:
        print(f"Error fetching alert details from Gemini: {e}")
        return []

async def update_alert_if_stale(alert_id: str) -> Optional[Alert]:
    alert = await retrieve_alert(alert_id)
    if not alert:
        return None

    now = datetime.utcnow()
    last_loaded = alert.meta.last_loaded if alert.meta else None
    if (not last_loaded) or (now - last_loaded > timedelta(days=1)):
        updated_data = await fetch_alert_details_from_gemini(alert_id)
        if updated_data:
            alert.message = updated_data.get("message", alert.message)
            alert.resources = updated_data.get("resources", alert.resources)
            alert.location = updated_data.get("location", alert.location)
            alert.timestamp = now
            if not alert.meta:
                alert.meta = MetaInfo()
            alert.meta.last_loaded = now
            await alert.save()
    return alert
