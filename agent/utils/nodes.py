from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from utils.states import State
from utils.tools import check_enquiry, get_available_timings
from datetime import datetime
from langchain import hub as prompts

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("passenger_id", None)
            state = {**state, "time": datetime.now, "user_info": passenger_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
primary_assistant_prompt = prompts.pull("realtor-assist:7a1c1eff")

part_1_tools = [check_enquiry, get_available_timings]
part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)