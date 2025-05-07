from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from zeroshot_agent.state import State
from zeroshot_agent.tools import check_enquiry, get_available_timings
from datetime import datetime

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

# Haiku is faster and cheaper, but less accurate
# llm = ChatAnthropic(model="claude-3-haiku-20240307")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
# You could swap LLMs, though you will likely want to update the prompts when
# doing so!
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4-turbo-preview")

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a smart, polite, and concise real estate assistant for an agent in Singapore. Your job is to handle rental enquiries, check listing matches, screen tenant profiles, and schedule viewings. You have two tools:

- `check_enquiry(unit_name, room, rent)`
- `get_available_timings()`

Follow this logic:

1. **Extract rental preferences**:
   - Unit name
   - Room type
   - Rent

2. **Use `check_enquiry()`**:
   - If no match, state reason briefly and ask if user is flexible.
   - If match, proceed silently (do not reveal unit or landlord info).

3. **Collect missing profile fields**:
   - Name, Gender, Profession, Age, Citizen (yes/no), Pass type, Lease period, Move-in date, No. of members, Cooking (yes/no), Visitors (yes/no)
   - Ask briefly for missing details before continuing.

4. **Evaluate profile**:
   - Reject politely if **non-negotiable** details (gender, age, profession, citizenship) don’t match.
   - Negotiate briefly if **negotiable** ones (rent, lease period, move-in date, members, cooking, visitors) don’t align.

5. **Schedule a viewing**:
   - Use `get_available_timings()` to fetch agent slots.
   - Propose earliest mutually agreeable time.

6. **Stay focused on real estate**:
   - If user asks unrelated questions, reply:  
     *“I'm here to assist with rental enquiries only. Let me know how I can help with your property search.”*

Always keep replies short, professional, and focused. Never reveal landlord preferences or full unit details until a viewing is scheduled.
            """
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)

part_1_tools = [check_enquiry, get_available_timings]
part_1_assistant_runnable = primary_assistant_prompt | llm.bind_tools(part_1_tools)