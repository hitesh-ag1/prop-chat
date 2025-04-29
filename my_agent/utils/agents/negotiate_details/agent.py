
from langchain.chat_models import init_chat_model
from langgraph.types import Command, interrupt
from typing import Literal
from langgraph.graph import END, StateGraph
from my_agent.settings import TEXT_MODEL
from my_agent.logging import logger
from my_agent.utils.prompts import negotiate_details_prompt
from langchain_core.messages import AIMessage
from my_agent.utils.agents.negotiate_details.model import (
    NegotiateDetails,
    State
)

llm = init_chat_model(TEXT_MODEL).with_structured_output(
    NegotiateDetails, 
    method="json_schema", 
    include_raw=True
)

async def negotiate_details_agent(state: State) -> Command[Literal[END]]:
    logger.info("-----Negotiate Details Agent-----")
    if "type" not in state['messages'][-2].additional_kwargs:
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
        match_details = {
            "match": state["match"],
            "negotiable": state["negotiable"],
            "keys": state["keys"]
        }
        llm_input = f"""
        landlord_preference = {str(landlord_preferences)}
        and
        user_profile = {str(user_profile)}
        and
        match_details = {str(match_details)}
        """
        print("-----Negotiate Details Agent-----")
        print(match_details)
        if state["negotiable"]:
            info = await llm.ainvoke(
                [
                    {"role": "system", "content": negotiate_details_prompt},
                    {"role": "user", "content": llm_input},
                    *state["messages"],
                ]
            )
            print(info['parsed'])
            parsed = info["parsed"]
            if parsed["end"]:
                if parsed["match"]:
                    goto = "appointment_agent"
                    return Command(goto=goto)
                # else:
                    # goto = END
                    # return Command(goto=goto)
            goto = "human_agent"
            messages = state["messages"] + [{"role":"assistant", "type":"negotiate", "content":info['parsed']['messages']}]
                        
            return Command(goto=goto, update={"category":"negotiate_details_agent", "messages": [AIMessage(content=info['parsed']['messages'])]})

            # return Command(update={"category":"negotiate_details_agent", "messages":messages}, goto=goto)
        else:
            goto = END
            return Command(goto=goto, update={"messages": [AIMessage(content="Sorry, no match brotha")]})
    else:
        print("-----Negotiate Details Agent 2-----")
        msgs = state["messages"][::-1]
        print(msgs)
        info = await llm.ainvoke(
                [
                    {"role": "system", "content": negotiate_details_prompt},
                    *msgs
                ]
            )
        
        parsed = info["parsed"]
        print(parsed)
        if parsed["end"]:
            if parsed["match"]:
                goto = "appointment_agent"
                return Command(goto=goto, update={"messages": [AIMessage(content=info['parsed']['messages'])]})
                # return Command(goto=goto)
            else:
                goto = END
                return Command(goto=goto, update={"messages": [AIMessage(content=info['parsed']['messages'])]})

                # return Command(goto=goto)
            
        goto = "human_agent"
        messages = state["messages"] + [{"role":"assistant", "type":"negotiate", "content":info['parsed']['messages']}]
        return {"messages": [AIMessage(content=info['parsed']['messages'])]}
        # return Command(update={"category":"negotiate_details_agent", "messages":messages}, goto=goto)
