from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from typing import Literal

class HumanState(TypedDict):
    """Human Agent state."""
    category: Literal["enquiry_extractor_agent" , "extract_profile_agent"]
    messages: Annotated[list[AnyMessage], add_messages]
