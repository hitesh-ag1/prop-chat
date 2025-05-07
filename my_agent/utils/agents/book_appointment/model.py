from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    """Agent state."""
    messages: Annotated[list[AnyMessage], add_messages]
    followup: str | None

    condo_name: str | None
    room_type: str | None
    rental_price: str | None

    listing_available: bool | None
    listing_details: list | None

    name: str | None
    gender: str | None
    profession: str | None
    age: str | None
    citizen: bool | None
    lease_period: str | None
    move_in_date: str | None
    num_members: str | None
    cooking: bool | None
    visitors: bool | None

    match: bool | None
    negotiable: bool | None
    keys: list[str] | None

    suggested_slots: list[str] | None
    user_slots: list[str] | None
    booked_slot: str | None

class AppointmentDetails(TypedDict):
    """Choose the best action along with message, suggested slots, user slots and booked slot."""

    message: str | None
    action: str | None
    suggested_slots: list[str] | None
    user_slots: list[str] | None
    booked_slot: str | None
