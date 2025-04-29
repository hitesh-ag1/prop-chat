from typing_extensions import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.types import Command, interrupt
from typing import Literal
from langgraph.graph import END, StateGraph
from my_agent.utils.agents.intent.model import IntentState, IntentExtract
from my_agent.utils.prompts import intent_agent_prompt
from my_agent.settings import TEXT_MODEL
from my_agent.logging import logger

llm = init_chat_model(TEXT_MODEL).with_structured_output(
    IntentExtract, 
    method="json_schema", 
    include_raw=True
)

async def intent_agent(state: IntentState) -> Command[END]:
    logger.info("-----Intent Agent-----")
    system_message = {"role": "system", "content": intent_agent_prompt}
    message_with_system = [system_message]+state["messages"]
    info = await llm.ainvoke(message_with_system)
    parsed = info["parsed"]
    goto = END
    if parsed["intent"]:
        goto = "enquiry_extractor_agent"
    return Command(goto=goto)