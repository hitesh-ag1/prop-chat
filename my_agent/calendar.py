import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pytz
import asyncio
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/calendar']
# creds = service_account.Credentials.from_service_account_file(
#     'service-account.json', scopes=SCOPES)

# service = build('calendar', 'v3', credentials=creds)


def _get_creds():
    creds = service_account.Credentials.from_service_account_file(
        'real-estate-bot.json',
        scopes=SCOPES               
    )
    service = build('calendar', 'v3', credentials=creds)
    return service


async def get_creds():
    
    res = await asyncio.to_thread(_get_creds)
    return res

async def get_timezone():
    sg_tz = await asyncio.to_thread(pytz.timezone('Asia/Singapore'))
    return sg_tz

class CalendarIntegration:
    def __init__(self, calendar_credential_file):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.calendar_credential_file = calendar_credential_file



    async def get_google_calendar_service(self):
        """Authenticate and build the Google Calendar service."""
        service = None
        # Check if the credentials file exists
        if os.path.exists(self.calendar_credential_file):
            service = await get_creds()
        return service

    def format_time_to_12hr(self, time_obj):
        """Format the time in 12-hour format with AM/PM."""
        return time_obj.strftime('%I:%M %p').lstrip('0')

    def format_date_with_day(self, date_obj):
        """Format the date with the day of the week."""
        return date_obj.strftime('%A, %d-%m-%Y')

    async def get_next_available_slot_from_calendar(self):
        """Find the next available slot in the calendar."""
        service = await self.get_google_calendar_service()
        sg_tz = pytz.timezone('Asia/Singapore')
        now_sg = datetime.now(sg_tz)
        work_start = sg_tz.localize(datetime.strptime("09:00", "%H:%M"))
        work_end = sg_tz.localize(datetime.strptime("21:00", "%H:%M"))
        today = now_sg.date()

        day_offset = 1
        while day_offset < 7:  # Check for the next 7 days
            target_date = today + timedelta(days=day_offset)

            for hour in range(9, 18):  # Check available slots between 9 AM and 6 PM
                potential_start_time = sg_tz.localize(datetime.combine(target_date, work_start.time()) + timedelta(hours=hour - 9))
                potential_end_time = potential_start_time + timedelta(hours=1)

                # Query all events that could overlap with this potential time slot
                events_result = service.events().list(
                    calendarId='primary',
                    timeMin=potential_start_time.isoformat(),
                    timeMax=potential_end_time.isoformat(),
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()

                events = events_result.get('items', [])
                
                available = True
                for event in events:
                    event_start = event['start'].get('dateTime')
                    event_end = event['end'].get('dateTime')

                    if event_start:
                        # Convert event times to Singapore Timezone
                        event_start_utc = datetime.fromisoformat(event_start.replace('Z', '+00:00'))
                        event_end_utc = datetime.fromisoformat(event_end.replace('Z', '+00:00'))
                        event_start_sg = event_start_utc.astimezone(sg_tz)
                        event_end_sg = event_end_utc.astimezone(sg_tz)

                        # Check if the event overlaps with the potential time slot
                        if (event_start_sg < potential_end_time and event_end_sg > potential_start_time):
                            available = False
                            break

                if available:
                    return potential_start_time, target_date
            day_offset += 1
        
        return None, None

    async def add_event_to_calendar(self, start_time, duration_hours=1):
        """Add an event to the calendar."""
        service = await self.get_google_calendar_service()

        if isinstance(start_time, datetime):
            end_time = start_time + timedelta(hours=duration_hours)

            event = {
                'summary': 'Scheduled Appointment',
                'location': 'Online',
                'description': 'Scheduled appointment by bot',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Singapore',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Singapore',
                },
                'attendees': [],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
            }

            created_event = service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event created: {created_event.get('htmlLink')}")
            print(created_event)
            return created_event
        else:
            raise ValueError("Start time must be a datetime object.")

    async def check_availability(self):
        """Check for the next available slot."""
        available_slot, available_date = await self.get_next_available_slot_from_calendar()
        
        if available_slot:
            formatted_time = self.format_time_to_12hr(available_slot.time())
            formatted_date_with_day = self.format_date_with_day(available_date)

            return {
                "is_avail": True,
                "date": formatted_date_with_day,
                "time": formatted_time,
                "message": f"Can we do scheduling on {formatted_date_with_day} at {formatted_time}."
            }
        else:
            return {
                "is_avail": False,
                "message": "No available slots for the next 7 days between 9 AM and 6 PM."
            }

    async def book_appointment(self, start_time):
        """Book an appointment using the stored date and time from the database."""
        appointment_duration_hours = 1  # Default 1-hour meeting duration
        
        # Create the event using the retrieved start time
        created_event = await self.add_event_to_calendar(start_time, appointment_duration_hours)

        formatted_time = self.format_time_to_12hr(start_time.time())
        formatted_date_with_day = self.format_date_with_day(start_time.date())

        return {
            "is_booked": True,
            "event_id": created_event['id'],
            "date": formatted_date_with_day,
            "time": formatted_time,
            "message": f"Appointment successfully booked on {formatted_date_with_day} at {formatted_time} SGT."
        }
