import json


FIELDS = [
    "job_title",
    "experience_years",
    "skills",
    "work_type"
]


def normalize_text(value):
    """Normalize text for comparison."""

    if value is None:
        return None

    return " ".join(str(value).strip().lower().split())


def parse_json_response(response):
    """
    Parse the model response as JSON.

    Returns:
        parsed JSON object, or None if invalid.
    """

    try:
        return json.loads(response)

    except (json.JSONDecodeError, TypeError):
        return None


def compare_field(predicted, expected):
    """Compare two non-list fields."""

    if predicted is None and expected is None:
        return 1.0

    if predicted is None or expected is None:
        return 0.0

    return float(
        normalize_text(predicted) == normalize_text(expected)
    )


def calculate_skill_metrics(predicted_skills, expected_skills):
    """Calculate precision, recall, and F1 for skills."""

    predicted = {
        normalize_text(skill)
        for skill in predicted_skills
    }

    expected = {
        normalize_text(skill)
        for skill in expected_skills
    }

    if not predicted and not expected:
        return 1.0, 1.0, 1.0

    if not predicted:
        return 0.0, 0.0, 0.0

    if not expected:
        return 0.0, 1.0, 0.0

    correct = predicted & expected

    precision = len(correct) / len(predicted)
    recall = len(correct) / len(expected)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = (
            2 * precision * recall
            / (precision + recall)
        )

    return precision, recall, f1


def evaluate_response(response, expected):
    """
    Evaluate one model response against ground truth.
    """

    parsed = parse_json_response(response)

    if parsed is None:
        return {
            "json_valid": False,
            "field_accuracy": 0.0,
            "skill_precision": 0.0,
            "skill_recall": 0.0,
            "skill_f1": 0.0,
            "completeness": 0.0,
            "overall_score": 0.0
        }

    field_scores = []

    for field in [
        "job_title",
        "experience_years",
        "work_type"
    ]:
        score = compare_field(
            parsed.get(field),
            expected.get(field)
        )

        field_scores.append(score)

    predicted_skills = parsed.get("skills", [])
    expected_skills = expected.get("skills", [])

    if not isinstance(predicted_skills, list):
        predicted_skills = []

    skill_precision, skill_recall, skill_f1 = (
        calculate_skill_metrics(
            predicted_skills,
            expected_skills
        )
    )

    field_accuracy = (
        sum(field_scores) + skill_f1
    ) / 4

    expected_item_count = 3 + len(expected_skills)

    correct_item_count = (
        field_scores[0]
        + field_scores[1]
        + field_scores[2]
        + len(
            {
                normalize_text(skill)
                for skill in predicted_skills
            }
            & {
                normalize_text(skill)
                for skill in expected_skills
            }
        )
    )

    completeness = (
        correct_item_count / expected_item_count
        if expected_item_count
        else 1.0
    )

    overall_score = (
        0.50 * field_accuracy
        + 0.30 * skill_f1
        + 0.20 * 1.0
    )

    return {
        "json_valid": True,
        "field_accuracy": field_accuracy,
        "skill_precision": skill_precision,
        "skill_recall": skill_recall,
        "skill_f1": skill_f1,
        "completeness": completeness,
        "overall_score": overall_score
    }
    
    
    
if __name__ == "__main__":

    expected = {
        "job_title": "Backend Developer",
        "experience_years": 3,
        "skills": [
            "Python",
            "FastAPI",
            "PostgreSQL"
        ],
        "work_type": "Remote"
    }

    response = """
    {
        "job_title": "Backend Developer",
        "experience_years": 3,
        "skills": ["Python", "FastAPI"],
        "work_type": "Remote"
    }
    """
    
    result = evaluate_response(
        response,
        expected
    )

    print(result)    