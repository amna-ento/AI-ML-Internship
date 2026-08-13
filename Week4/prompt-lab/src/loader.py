import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "test_cases.json"
PROMPTS_PATH = PROJECT_ROOT / "prompts"


def load_test_cases():
    """Load all test cases and ground truths."""

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_prompt(prompt_name: str):
    """Load and validate a prompt template."""

    prompt_path = PROMPTS_PATH / f"{prompt_name}.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()

    if "{{input}}" not in prompt:
        raise ValueError(
            f"Prompt '{prompt_name}' does not contain {{input}} placeholder."
        )

    return prompt


def build_prompt(prompt_template: str, job_description: str):
    """Insert a job description into a prompt template."""

    return prompt_template.replace(
        "{{input}}",
        job_description
    )
    
    
    
if __name__ == "__main__":
    test_cases = load_test_cases()

    print("Test cases loaded:", len(test_cases))

    prompt = load_prompt("naive")

    print("Naive prompt loaded successfully.")

    final_prompt = build_prompt(
        prompt,
        test_cases[0]["input"]
    )

    print("\nFinal prompt:")
    print(final_prompt)    