from typing_extensions import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.types import Command, interrupt
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt, ActionRequest
from typing import Literal
from langgraph.graph import END, StateGraph


class HumanState(TypedDict):
    """Human Agent state."""
    category: Literal["enquiry_extractor_agent" , "extract_profile_agent"]
    messages: Annotated[list[AnyMessage], add_messages]

def human_node(state: HumanState) -> Command[Literal["match_profile_agent", "extract_profile_agent", "enquiry_extractor_agent", END]]:
    print("-----Human Agent-----")
    print(state['category'])
    print(state['messages'])
    # answer = interrupt(
    #     state['messages'][-1].content
    # )
    # update = {
    #         "messages": state['messages']+[{"role":"human", "content":answer}]
    #         }
    # print(answer, state['category'])

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
    print("-----Response-----")
    print(response)
    update = {
        "messages": state['messages'] + [{"role": "human", "content": response["args"]}]
    }

    return Command(update=update, goto=state['category'])
