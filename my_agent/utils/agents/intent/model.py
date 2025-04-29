from typing_extensions import Annotated, TypedDict

class IntentState(TypedDict):
    """Intent Agent state."""
    intent: bool | None

class IntentExtract(TypedDict):
    """Classify whether the user message is related to a real estate listing or not. Do not make up values, leave fields as null if you don't know their value."""

    intent: bool | None
    followup: Annotated[
        str | None,
        ...,
        "If the user hasn't enough identifying information, please tell them what the required information is and ask them to specify it.",
    ]
