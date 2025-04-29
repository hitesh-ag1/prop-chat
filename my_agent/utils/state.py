from langgraph.graph import add_messages
from my_agent.utils.memory_crud import patch_profile, add_enquiries
from typing import TypedDict, Annotated, Sequence, List, Dict

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    profile: Annotated[Dict, patch_profile]
    enquiries: Annotated[Dict, add_enquiries]
