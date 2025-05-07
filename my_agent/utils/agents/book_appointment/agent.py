from langchain.chat_models import init_chat_model
from langgraph.graph import END
from langchain_core.messages import AIMessage, HumanMessage
from my_agent.utils.agents.book_appointment.helper import (
    get_availability, book_event, check_timeslot_availability
)
from my_agent.settings import TEXT_MODEL
from my_agent.utils.agents.book_appointment.model import AppointmentDetails, State
from langgraph.types import Command
from my_agent.logging import logger
from datetime import datetime
from zoneinfo import ZoneInfo


tools = [get_availability, book_event, check_timeslot_availability]
llm = init_chat_model(TEXT_MODEL)
llm.bind_tools(tools)
llm = llm.with_structured_output(
    AppointmentDetails, method="json_schema", include_raw=True
)

APPT_SYSTEM_PROMPT = """
You are a world-class AI assistant for booking house viewing appointments for real estate agents. Your goal is to find a suitable time slot for both the user and the agent, and book an appointment. 
You have access to the agent's availability using the 'get_availability' and 'check_timeslot_availability' tools. You can also book an appointment using the 'book_event' tool.

Suggest few time slots for the user according to agent's availability. 
If the user has a specific time in mind, check if it's available. If it is, book it. If not, suggest an alternate time slot according to agent's availability.

Always respond in this JSON structure:
{
  "message": "<friendly, concise message>",
  "action": "<one of continue, end>",
  "suggested_slots": "<(optional) slots (ISO 8601) you're offering>",
  "user_slots": "<(optional) user-requested slots (ISO 8601)>",
  "booked_slot": "<(optional) booked slot (ISO 8601)>",
}

Definitions:
- confirm_and_book: The user accepted a suggested slot; tell the user it's being booked.
- suggest_alternate: The user requested a different time. Suggest a specific available slot.
- user_preference: The user has a specific time in mind. Check if it's available. If not, suggest an alternate time slot.
- abort: The user wants to cancel or exit.

Never make up or invent available slots. Only use those provided (from 'get_availability' and 'check_timeslot_availability').
Do not add extra explanation outside the JSON. Be concise, polite, and helpful as a top-tier helpful assistant.
"""

def flatten_slot_dict(availability_dict):
    """Return a flat list of datetime strings from availability dict."""
    slots = []
    for day_slots in availability_dict.values():
        slots.extend(day_slots)
    return slots

def slot_within_next_3_days(slot_str):
    now = datetime.now()
    try:
        slot = datetime.strptime(slot_str, "%Y-%m-%d %H:%M")
    except:
        return False
    delta = slot - now
    return 0 <= delta.days < 3

async def book_appointment(state: State):
        logger.info("-----Book Appointment Agent-----")
        msgs = state["messages"][::-1]
        print(msgs)
        message = await llm.ainvoke(
                [
                    {"role": "system", "content": APPT_SYSTEM_PROMPT},
                    *msgs
                ]
            )
        
        parsed = message["parsed"]
        print(parsed)
        return Command(
            update={
                "messages": [
                    *msgs,
                    AIMessage(
                        content=parsed['message']
                    )
                ],
                "suggested_slots": parsed['suggested_slots'],
                "user_slots": parsed['user_slots'],
                "booked_slot": parsed['booked_slot'],
                "action": parsed['action'],
                "category": "appointment_agent",
            },
            goto="human_agent",
        )
    # else:
    #     return Command(goto=END, update={"messages": [AIMessage(content=state['messages'][-1].content)]})
