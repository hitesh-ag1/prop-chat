from langgraph.types import Command, interrupt
from typing import Literal
from langgraph.graph import END, StateGraph
from langchain.schema import AIMessage
from my_agent.utils.agents.check_profile.model import (
    State,
)
from my_agent.logging import logger


async def profile_chk_agent(state: State) -> Command[Literal["human_agent", "match_profile_agent", END]]:
    logger.info("-----Profile Check Agent-----")
    profile = ["name", "gender", "profession", "age", "citizen", "lease_period", "move_in_date", "num_members", "cooking", "visitors"]
    if all(k in state and state[k]!=None for k in profile):
        goto = "match_profile_agent"
        return Command(update={}, goto=goto)
    else:
        required_fields = []
        for k in profile:
            if k not in state:
                required_fields.append(k)
        response = "Please provide the following profile details: " + ', '.join(required_fields)
        goto = "human_agent"
        flag=True
        messages = state["messages"]
        for msg in state["messages"]:
            if isinstance(msg, AIMessage) and (msg.content == response):
                flag=False
        if flag:
            messages = state["messages"] + [{"role":"assistant", "content":response}]
        return Command(update={"category":"extract_profile_agent", "messages":messages}, goto=goto)
