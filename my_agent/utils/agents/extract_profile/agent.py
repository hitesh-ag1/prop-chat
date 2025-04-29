
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from my_agent.settings import TEXT_MODEL
from my_agent.utils.prompts import profile_extractor_prompt
from my_agent.utils.agents.extract_profile.model import (
    ProfileExtract,
    State,
)
from my_agent.logging import logger


llm = init_chat_model(TEXT_MODEL).with_structured_output(
    ProfileExtract, method="json_schema", include_raw=True
)

async def extract_profile_agent(state: State) -> Command[Literal[END]]:
    logger.info("-----Profile Extract Agent-----")
    info = await llm.ainvoke(
        [
            {"role": "system", "content": profile_extractor_prompt},
            *state["messages"],
        ]
    )
    parsed = info["parsed"]
    profile = ["name", "gender", "profession", "age", "citizen", "lease_period", "move_in_date", "num_members", "cooking", "visitors"]
    if all(parsed[k]!=None for k in profile):
        update = parsed
        goto = "check_profile_agent"
        return Command(update=update, goto=goto)
