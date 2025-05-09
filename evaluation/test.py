from langsmith import Client
import os
from helper import predict, accuracy, conciseness, hallucination

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
dataset_name = "primary"

results = client.evaluate(
    predict,
    data=dataset_name,
    evaluators=[accuracy, conciseness, hallucination],
    experiment_prefix="v2",
    description="Evaluating accuracy, conciseness and hallucination of a simple prediction model.",
    metadata={
        "prompt-version": "v2",
    },
)
