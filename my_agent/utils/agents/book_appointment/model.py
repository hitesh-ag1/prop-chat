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

# class NegotiateDetails(TypedDict):
#     """Negotiate the details with the user. Do not make up values, leave fields as null if you don't know their value."""
    
#     match: bool | None
#     messages: str | None
#     end: bool | None

#     followup: Annotated[
#         str | None,
#         ...,
#         "If any errors occur, please tell them here.",
#     ]
