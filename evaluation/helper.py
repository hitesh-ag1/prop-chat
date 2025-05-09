from langsmith.schemas import Example, Run
from langchain_community.adapters.openai import convert_openai_messages
from langchain import hub as prompts
import os
from dotenv import load_dotenv
from openevals.llm import create_llm_as_judge
from openevals.prompts import CONCISENESS_PROMPT, CORRECTNESS_PROMPT, HALLUCINATION_PROMPT

load_dotenv()

part_1_assistant_runnable = prompts.pull("realtor-assist:7a1c1eff", include_model=True, api_key=os.getenv("LANGSMITH_API_KEY"))

correctness_evaluator = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    continuous=True,
    feedback_key="correctness",
    model="openai:o3-mini",
)

conciseness_evaluator = create_llm_as_judge(
    prompt=CONCISENESS_PROMPT,
    continuous=True,
    feedback_key="conciseness",
    model="openai:o3-mini",
)

hallucination_evaluator = create_llm_as_judge(
    prompt=HALLUCINATION_PROMPT,
    continuous=True,
    feedback_key="hallucination",
    model="openai:o3-mini",
)

def accuracy(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    input = inputs["messages"]
    pred = outputs["prediction"]
    expected = reference_outputs["expected"]
    return correctness_evaluator(
        inputs=str(input),
        outputs=pred,
        reference_outputs=expected
    )

def conciseness(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    input = inputs["messages"]
    pred = outputs["prediction"]
    expected = reference_outputs["expected"]
    return conciseness_evaluator(
        inputs=str(input),
        outputs=pred,
        reference_outputs=expected
    )

def hallucination(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    input = inputs["messages"]
    pred = outputs["prediction"]
    expected = reference_outputs["expected"]
    return hallucination_evaluator(
        inputs=str(input),
        outputs=pred,
        context="You are evaluating response as a real estate agent who is assisting a customer with rental enquiries and matching profiles according to landlord preferences.",
        reference_outputs=expected
    )

def predict(inputs: dict) -> dict:
    out = part_1_assistant_runnable.invoke(
        {
            "time": inputs["time"],
            "messages": convert_openai_messages(inputs["messages"]),
        }
    )
    return {
            "prediction": out.content,
        }
