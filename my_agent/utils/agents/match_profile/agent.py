from langchain.chat_models import init_chat_model
from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from my_agent.utils.prompts import profile_matcher_prompt
from my_agent.settings import TEXT_MODEL
from my_agent.logging import logger
from langchain_core.messages import AIMessage
from my_agent.utils.agents.match_profile.model import (
    ProfileMatch,
    State
)

llm = init_chat_model(TEXT_MODEL).with_structured_output(
    ProfileMatch, 
    method="json_schema", 
    include_raw=True
)

async def match_profile_agent(state: State) -> Command[Literal[END]]:
    logger.info("-----Match Profile Agent-----")
    user_profile = {
        "name": state["name"],
        "gender": state["gender"],
        "profession": state["profession"],
        "age": state["age"],
        "citizen": state["citizen"],
        "lease_period": state["lease_period"],
        "move_in_date": state["move_in_date"],
        "num_members": state["num_members"],
        "cooking": state["cooking"],
        "visitors": state["visitors"]
    }
    landlord_preferences = state['listing_details'][0]['Landlord Profile Preferences']
    llm_input = f"""
    landlord_preference = {str(landlord_preferences)}
    and
    user_profile = {str(user_profile)}
    """

    info = await llm.ainvoke(
        [
            {"role": "system", "content": profile_matcher_prompt},
            {"role": "user", "content": llm_input},
            *state["messages"],
        ]
    )
    parsed = info["parsed"]
    if parsed["match"]:
        print("Profile Matched")
        goto='appointment_agent'
        return {"messages": [AIMessage(content="Profile matched bud, thanks")]}
        # return Command(update=parsed, goto=goto)
    else:
        print("Profile Not Matched")
        goto='negotiate_details_agent'
        return Command(update=parsed, goto=goto)
