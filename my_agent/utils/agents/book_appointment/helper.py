# from my_agent.calendar import CalendarIntegration
from datetime import datetime, timedelta, time
import random
from typing import List, Dict

# calendar_credential_file = './token.json'
# calendar_integration = CalendarIntegration(calendar_credential_file)


# async def get_availability():
#     availability_response = await calendar_integration.check_availability()
#     return availability_response


# async def book_event(datetime: datetime):
#     availability_response = await calendar_integration.book_appointment(datetime)
#     return availability_response['message']

def _generate_timeslots(date: datetime) -> List[str]:
    """Generate 3 standard timeslots for a given date."""
    slots = [time(9, 0), time(13, 0), time(16, 0)]
    return [
        datetime.combine(date.date(), slot_time).strftime('%Y-%m-%d %H:%M')
        for slot_time in slots
    ]

async def get_availability() -> Dict[str, List[str]]:
    """
    LangGraph Tool: Get three standard appointment timeslots for each of the next three days.
    Returns a dict mapping date (YYYY-MM-DD) to available timeslot start times.
    """
    availability = {}
    today = datetime.now()
    for i in range(3):  # today + next 2 days
        day = today + timedelta(days=i)
        slots = _generate_timeslots(day)
        availability[day.strftime('%Y-%m-%d')] = slots
    return availability

async def check_timeslot_availability(timeslots: List[str]) -> Dict[str, bool]:
    """
    LangGraph Tool: Check whether a list of timeslots are available.
    """
    return {slot: random.choice([True, False]) for slot in timeslots}

async def book_event(timeslot: str) -> str:
    """
    LangGraph Tool: Book an appointment at a given timeslot.
    """
    return f"Booking confirmed for {timeslot}"
