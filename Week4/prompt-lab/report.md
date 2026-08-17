# project Report

## Project Overview

This project evaluates different prompt engineering strategies for extracting structured information from unstructured job descriptions.

The goal was to determine which prompting strategy produces the most accurate, consistent, and machine-readable results.

Four prompt strategies were implemented and evaluated:

1. Naive Prompt
2. Few-Shot Prompt
3. Reasoning Prompt
4. Structured Output Prompt

Each prompt was tested against the same set of 20 job descriptions, resulting in a total of 80 evaluations.

The extracted information included:

- Job title
- Required years of experience
- Skills
- Work type

The outputs were automatically evaluated using predefined metrics such as JSON validity, field accuracy, skill precision, skill recall, skill F1-score, completeness, and overall score.

---

## Task Definition

### Problem

Job descriptions are typically written as unstructured natural language. Extracting important information from them manually can be time-consuming and inconsistent.

The task in this project is to automatically extract the following information from each job description:

- **Job Title**
- **Required Experience in Years**
- **Skills**
- **Work Type**

### Example Input

Data Science Director needed to lead product strategy and analytics vision. Must know Generative ML, Discriminative ML, Contrastive ML, Classification, Gradient Boosting, Causal Inference, AI, and advanced statistics. 8+ years of experience required. Full-time position.

### Expected Output

```json
{
  "job_title": "Data Science Director",
  "experience_years": 8,
  "skills": [
    "Generative ML",
    "Discriminative ML",
    "Contrastive ML",
    "Classification",
    "Gradient Boosting",
    "Causal Inference",
    "AI",
    "advanced statistics"
  ],
  "work_type": "Full-time"
}
```

## Objective

The primary objective is to compare the four prompting strategies and determine which approach provides the best performance for reliable structured information extraction.


# Bash Commands and Results

This section documents the terminal commands used to run, validate, and evaluate the prompt experiments. It allows anyone reviewing the project to reproduce the evaluation process and understand the reported results.

---

## 1. Activate the Virtual Environment

### Command

```bash
source /Users/amento/Desktop/AI-ML-Internship/Week4/prompt-lab/.venv/bin/activate
```
## Purpose

Activates the project's Python virtual environment so that all required dependencies are available.

Result
```bash
(.venv) amento@AmentoMacBook-M2 prompt-lab %
```

The (.venv) prefix confirms that the virtual environment is active.

# Run the Test Case Loader
 ```bash
 python src/loader.py
 ```

## Purpose

Loads the 20 job-description test cases and verifies that the prompt files can be loaded correctly.

### Result
Test cases loaded: 20
Naive prompt loaded successfully.

### Final prompt:
Extract the job title, required experience in years, skills, and work type from the following job description.

### Job description:
Data Science Director needed to lead product strategy and analytics vision. Must know Generative ML, Discriminative ML, Contrastive ML, Classification, Gradient Boosting, Causal Inference, AI, and advanced statistics. 8+ years of experience required. Full-time position.

### Interpretation 
- 20 test cases were successfully loaded.
- The prompt loader successfully found and loaded the naive prompt.
- The system was able to construct a final prompt using a job description.



# Verify Number of Results
Command
```bash
python -c "import json; print(len(json.load(open('results/results.json'))))"
```
## Purpose

Checks how many experiment results were stored in results/results.json.

## Result
80
## Interpretation

There are: 20 test cases, 4 prompt strategies
Therefore:

20 × 4 = 80 results

This confirms that all four prompt strategies were executed against all 20 test cases.

# Validate JSON Output
Command
```bash
python -c "import json; from collections import defaultdict; r=json.load(open('results/results.json')); d=defaultdict(list); [(d[x['prompt']].append(x['evaluation']['json_valid'])) for x in r]; [(print(k, 'Valid JSON:', sum(v), '/', len(v))) for k,v in d.items()]"
```
## Purpose

Measures how often each prompt strategy produced valid JSON output.

## Result
- naive Valid JSON: 0 / 20
- few_shot Valid JSON: 2 / 20
- reasoning Valid JSON: 0 / 20
- structured Valid JSON: 20 / 20

# 5. Calculate Mean Overall Score

### Command

```bash
python -c "import json, statistics; from collections import defaultdict; r=json.load(open('results/results.json')); d=defaultdict(list); [(d[x['prompt']].append(x['evaluation']['overall_score'])) for x in r]; [(print(k, 'Mean Overall Score:', round(statistics.mean(v),3))) for k,v in d.items()]"
```
## Purpose

Calculates the average overall evaluation score for each prompt strategy across all 20 test cases.

## Result
- naive Mean Overall Score: 0.0
- few_shot Mean Overall Score: 0.087
- reasoning Mean Overall Score: 0.0
- structured Mean Overall Score: 0.969

# Calculate Detailed Evaluation Metrics
Command
```bash
python -c "import json, statistics; from collections import defaultdict; r=json.load(open('results/results.json')); d=defaultdict(list); [(d[x['prompt']].append(x['evaluation'])) for x in r]; [(print('\n',k, '\nField Accuracy:', round(statistics.mean([x['field_accuracy'] for x in v]),3), '\nSkill Precision:', round(statistics.mean([x['skill_precision'] for x in v]),3), '\nSkill Recall:', round(statistics.mean([x['skill_recall'] for x in v]),3), '\nSkill F1:', round(statistics.mean([x['skill_f1'] for x in v]),3), '\nCompleteness:', round(statistics.mean([x['completeness'] for x in v]),3), '\nOverall:', round(statistics.mean([x['overall_score'] for x in v]),3))) for k,v in d.items()]"
```
## Purpose

Calculates the average performance of each prompt strategy across all evaluation metrics.

## Final Evaluation Summary

The results of all four prompting strategies are summarized below.

| Metric            | Naive | Few shot | Reasoning | Structured |
|-------------------|------:|---------:|----------:|----------:|
| Valid JSON        | 0/20  | 2/20     | 0/20      | **20/20** |
| Field Accuracy    | 0.000 | 0.075    | 0.000     | **0.946** |
| Skill Precision   | 0.000 | 0.100    | 0.000     | **0.976** |
| Skill Recall      | 0.000 | 0.100    | 0.000     | **1.000** |
| Skill F1          | 0.000 | 0.100    | 0.000     | **0.986** |
| Completeness      | 0.000 | 0.087    | 0.000     | **0.977** |
| Overall Score     | 0.000 | 0.087    | 0.000     | **0.969** |




# Key Findings

The experiment shows a clear difference between the four prompting strategies.

## Naive Prompt

The naive prompt produced human-readable answers, but they were not consistently valid JSON. Because the evaluation requires machine-readable structured output, the results received a score of 0.000.

## Few-shot Prompt

The few-shot prompt performed slightly better than the naive prompt, but only 2/20 outputs were valid JSON. Its average overall score was only 0.087.

## Reasoning Prompt

The reasoning prompt produced descriptive answers such as tables and JSON code blocks rather than the exact machine-readable format required by the evaluator. As a result, it achieved 0/20 valid JSON outputs and an overall score of 0.000.

## Structured Prompt

The structured-output prompt performed significantly better.


## Why the Structured Prompt Won

The Structured Output Prompt achieved the best performance across all evaluation metrics.

- It produced **20/20 valid JSON outputs**, compared with 0/20 for the Naive Prompt, 2/20 for the Few-Shot Prompt, and 0/20 for the Reasoning Prompt.
- It achieved the highest **Field Accuracy (0.946)**, showing that the extracted job information closely matched the ground truth.
- It achieved **1.000 Skill Recall**, meaning it successfully extracted all expected skills on average.
- It achieved **0.986 Skill F1**, showing a strong balance between correctly identifying skills and avoiding incorrect skills.
- It achieved the highest **Completeness score (0.977)**.
- Its **Overall Score of 0.969** was substantially higher than Few-shot (0.087), Naive (0.000), and Reasoning (0.000).

The Structured Prompt performed best because this task requires the model to return multiple specific fields in a predictable, machine-readable format. By explicitly defining the required JSON schema and instructing the model to return only valid JSON with no additional text, the prompt reduced formatting errors and missing information.

Therefore, the experimental results support using structured-output prompting for this type of information extraction task.


# Conclusion

The experiment demonstrates that prompt design has a significant impact on the reliability of LLM-based information extraction.

For this job-description extraction task, enforcing a strict structured-output format resulted in substantially better performance than naive, few-shot, and reasoning-based prompts.

The final ranking was:

- Structured Prompt — 0.969
- Few-shot Prompt — 0.087
- Naive Prompt — 0.000
- Reasoning Prompt — 0.000

The results support using structured-output prompting when LLM responses need to be consumed programmatically by downstream applications.