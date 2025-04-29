from langchain.chat_models import init_chat_model
from langgraph.types import Command, interrupt
from typing import Literal
from langgraph.graph import END, StateGraph
from my_agent.utils.agents.extract_enquiry.model import (
    EnquiryState,
    EnquiryExtract,
)
from my_agent.utils.prompts import enquiry_extractor_prompt
from my_agent.logging import logger
from my_agent.settings import TEXT_MODEL

llm = init_chat_model(TEXT_MODEL).with_structured_output(
    EnquiryExtract, 
    method="json_schema", 
    include_raw=True
)


async def enquiry_extractor_agent(state: EnquiryState) -> Command[Literal["check_enquiry_agent", "human_agent", END]]:
    logger.info("-----Enquiry Extract Agent-----")
    info = await llm.ainvoke(
        [
            {"role": "system", "content": enquiry_extractor_prompt},
            *state["messages"],
        ]
    )

    parsed = info['parsed']
    goto=END

    if all(parsed[k] for k in ("condo_name", "room_type", "rental_price")):
        goto = "check_enquiry_agent"
        info["messages"] = state["messages"]
        update = parsed
        update["messages"] = state["messages"]
    else:
        unavailable = []
        for k in ("condo_name", "room_type", "rental_price"):
            if not parsed[k]:
                unavailable.append(k)
        response = "Please provide the following details: " + ', '.join(unavailable)
        goto = "human_agent"
        messages = state["messages"] + [{"role":"assistant", "content":response}]
        update = {"category":"enquiry_extractor_agent", "messages":messages}
    
    return Command(update=update, goto=goto)
