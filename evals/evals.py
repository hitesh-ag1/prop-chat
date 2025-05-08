from langsmith.evaluation import LangChainStringEvaluator, evaluate
from helper import predict, format_evaluator_inputs
from openevals.llm import create_llm_as_judge
from openevals.prompts import CONCISENESS_PROMPT, CORRECTNESS_PROMPT

dataset_names = ["enquiry_eval", "profile_eval"]

correctness_evaluator = LangChainStringEvaluator(
    "labeled_score_string",
    config={"criteria": "correctness", "normalize_by": 10},
    prepare_data=format_evaluator_inputs,
)

# correctness_evaluator = create_llm_as_judge(
#     prompt=CORRECTNESS_PROMPT,
#     feedback_key="correctness",
#     model="openai:o3-mini",
# )

# conciseness_evaluator = create_llm_as_judge(
#     prompt=CONCISENESS_PROMPT,
#     feedback_key="conciseness",
#     model="openai:o3-mini",
# )

for dataset in dataset_names:
    results = evaluate(
        predict,
        data=dataset,
        experiment_prefix="prompt1",
        evaluators=[correctness_evaluator],
        # prepare_data=format_evaluator_inputs,
    )