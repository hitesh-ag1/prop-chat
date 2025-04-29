from langgraph.types import Command, interrupt
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt, ActionRequest
from typing import Literal
from langgraph.graph import END
from my_agent.utils.agents.human_interrupt.model import HumanState
from my_agent.logging import logger

def human_node(state: HumanState) -> Command[Literal["match_profile_agent", "extract_profile_agent", "enquiry_extractor_agent", END]]:
    logger.info("-----Human Agent-----")
    # Extract a tool call from the state and create an interrupt request
    request = HumanInterrupt(
        action_request=ActionRequest(
            action="Provide Details",  # The action being requested
            args={"sample":"Return these values"}  # Arguments for the action
        ),
        config=HumanInterruptConfig(
            allow_respond=True,
            allow_edit=False,
            allow_accept=False,
            allow_ignore= True,
        ),
        description=state['messages'][-1].content
    )
    # Send the interrupt request and get the response
    response = interrupt([request])[0]
    logger.info("-----Response-----")
    update = {
        "messages": state['messages'] + [{"role": "human", "content": response["args"]}]
    }

    return Command(update=update, goto=state['category'])
