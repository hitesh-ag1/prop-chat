from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from zeroshot_agent.agent import Assistant, part_1_assistant_runnable, part_1_tools
from zeroshot_agent.utils import create_tool_node_with_fallback
from zeroshot_agent.state import State
from langfuse.callback import CallbackHandler
import os
import uuid

builder = StateGraph(State)

# Define nodes: these do the work
builder.add_node("assistant", Assistant(part_1_assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

langfuse_handler = CallbackHandler(
    public_key=os.getenv('LANGFUSE_PUBLIC_KEY'), 
    secret_key=os.getenv('LANGFUSE_SECRET_KEY'), 
    host=os.getenv('LANGFUSE_HOST'),
    session_id=str(uuid.uuid4()),
)
part_1_graph = builder.compile().with_config({"callbacks": [langfuse_handler]})