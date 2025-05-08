from langsmith.schemas import Example, Run
from langchain_community.adapters.openai import convert_openai_messages
from langchain import hub as prompts
import os
from dotenv import load_dotenv

load_dotenv()

part_1_assistant_runnable = prompts.pull("realtor-assist:a8dcb23e", include_model=True, api_key=os.getenv("LANGSMITH_API_KEY"))

def predict(inputs: dict):
    return part_1_assistant_runnable.invoke(
        {
            "time": inputs["time"],
            "messages": convert_openai_messages(inputs["messages"]),
        }
    )

def format_evaluator_inputs(run: Run, example: Example):
    return {
        "input": example.inputs,
        "prediction": next(iter(run.outputs.values())),
        "reference": example.outputs["expected"],
    }

