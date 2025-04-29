from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import AnyMessage, add_messages

class EnquiryExtract(TypedDict):
    """
    All of the known information about the listing enquiry the user would like to know. \
    Do NOT make up values, leave fields as NULL if you don't know their value. \
    Do NOT set rental_price as 0 if not provided, instead let it be None. \
    """

    condo_name: str | None
    room_type: str | None
    rental_price: str | None

    followup: Annotated[
        str | None,
        ...,
        "If the user hasn't enough identifying information, please tell them what the required information is and ask them to specify it.",
    ]


class EnquiryState(TypedDict):
    """Enquiry Agent state."""
    messages: Annotated[list[AnyMessage], add_messages]
    followup: str | None

    condo_name: str | None
    room_type: str | None
    rental_price: str | None

