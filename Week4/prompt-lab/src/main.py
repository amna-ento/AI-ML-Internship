import json
from pathlib import Path

from loader import load_test_cases, load_prompt, build_prompt
from llm import generate_response
from evaluator import evaluate_response


PROMPT_NAMES = [
    "naive",
    "few_shot",
    "reasoning",
    "structured"
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_FILE = RESULTS_DIR / "results.json"


def run_experiment():
    """Run all prompts against all test cases."""

    test_cases = load_test_cases()
    

    print(f"Loaded {len(test_cases)} test cases.")
    print(f"Running {len(PROMPT_NAMES)} prompts.")
    print(f"Total evaluations: {len(test_cases) * len(PROMPT_NAMES)}")
    print()

    RESULTS_DIR.mkdir(exist_ok=True)

    results = []

    total = len(test_cases) * len(PROMPT_NAMES)
    current = 0

    for prompt_name in PROMPT_NAMES:

        print(f"\n--- Running {prompt_name} prompt ---")

        prompt_template = load_prompt(prompt_name)

        for test_case in test_cases:

            current += 1

            test_id = test_case["id"]
            job_description = test_case["input"]
            expected = test_case["expected"]

            print(
                f"[{current}/{total}] "
                f"{prompt_name} → Test {test_id}"
            )

            final_prompt = build_prompt(
                prompt_template,
                job_description
            )

            response = generate_response(final_prompt)

            evaluation = evaluate_response(
                response,
                expected
            )

            results.append({
                "test_id": test_id,
                "prompt": prompt_name,
                "input": job_description,
                "expected": expected,
                "response": response,
                "evaluation": evaluation
            })

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("Experiment completed.")
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    run_experiment()