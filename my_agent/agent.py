from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END

from my_agent.utils.agents.intent.agent import intent_agent
from my_agent.utils.agents.extract_enquiry.agent import enquiry_extractor_agent
from my_agent.utils.agents.check_enquiry.agent import enquiry_chk_agent
from my_agent.utils.agents.check_profile.agent import profile_chk_agent
from my_agent.utils.agents.extract_profile.agent import extract_profile_agent
from my_agent.utils.agents.match_profile.agent import match_profile_agent
from my_agent.utils.agents.negotiate_details.agent import negotiate_details_agent
from my_agent.utils.agents.human_interrupt.agent import human_node

from my_agent.utils.state import AgentState

from my_agent.logging import logger
from my_agent.utils.agents.negotiate_details.model import State 


# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["openai"]

# Define config
config = {"configurable": {"thread_id": "2"}}

    
def should_continue(state):
    messages = state["messages"]
    if len(messages) > 6:
        return "end"
    elif messages[-1].content == "FINISHED":
        return "end"
    else:
        return "continue"

# checkpointer = asyncio.run(init_db_pool())

# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Define the two nodes we will cycle between
workflow.add_node("intent_classifier", intent_agent)
workflow.add_node("enquiry_extractor_agent", enquiry_extractor_agent)
workflow.add_node("check_enquiry_agent", enquiry_chk_agent)
workflow.add_node("check_profile_agent", profile_chk_agent)
workflow.add_node("human_agent", human_node)
workflow.add_node("extract_profile_agent", extract_profile_agent)
workflow.add_node("match_profile_agent", match_profile_agent)
workflow.add_node("negotiate_details_agent", negotiate_details_agent)
# workflow.add_node("schedule_appointment_agent", schedule_appointment_agent)
# workflow.add_node("negotiate_details_agent", negotiate_details_agent)
# workflow.add_node("compile_followup", compile_followup)

workflow.set_entry_point("intent_classifier")

graph = workflow.compile()