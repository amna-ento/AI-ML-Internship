# The Prompt Lab — Task Plan

## 1. What is this task asking us to build?

We need to build a small **CLI (Command Line Interface) tool** that tests different prompting techniques on the **same task and same 20 inputs**.

The main goal is NOT just to show that we know different prompting techniques.

The important part is:

> We need to experimentally compare four different prompts and use actual scores to decide which prompt works best.

So this is basically a small **Prompt Engineering experiment**.

---

# 2. Overall idea

We will choose ONE task.

For example:

> Extract structured information from unstructured job descriptions.

Suppose one input is:

"Python Developer needed with 2+ years of experience. Must know FastAPI and PostgreSQL. Remote position."

We want the model to extract something like:

{
    "job_title": "Python Developer",
    "experience_years": 2,
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "work_type": "Remote"
}

Then we will ask the LLM to perform this SAME task using four different prompts.

---

# 3. The four prompt versions

We need exactly four versions.

## Prompt 1 — Naive

This is the simplest possible prompt.

Example idea:

"Extract the job title, required experience, skills, and work type from this job description."

No examples.

No special structure.

No advanced prompting technique.

Purpose:

> Establish a baseline.

This tells us how well the model performs with a basic prompt.

---

## Prompt 2 — Few-shot

Here we give the model a few examples before giving it the real input.

For example:

Example 1:

Input:
"Data Scientist with 3 years of Python and SQL experience."

Output:
{
    "job_title": "Data Scientist",
    "experience_years": 3,
    "skills": ["Python", "SQL"]
}

Then another example.

Then the actual job description.

Purpose:

> See whether examples help the model understand the task better.

---

## Prompt 3 — Chain-of-thought

Here we ask the model to reason through the problem before producing the answer.

Conceptually:

1. Identify the job title.
2. Find experience requirements.
3. Identify technical skills.
4. Identify work arrangement.
5. Produce the final answer.

Important:

We should be careful about how we implement this.

For our experiment, we can ask the model for a concise reasoning process or intermediate analysis rather than trying to capture hidden reasoning.

The important thing is to test whether adding a reasoning step improves extraction accuracy.

Purpose:

> Test whether breaking the reasoning into steps improves results.

---

## Prompt 4 — Structured-output-enforced

Here we strongly enforce the output format.

For example:

Return ONLY valid JSON using this schema:

{
    "job_title": "string",
    "experience_years": "number or null",
    "skills": ["string"],
    "work_type": "string or null"
}

No explanation.

No extra text.

Purpose:

> Test whether strict output instructions make the results more consistent and easier to evaluate automatically.

---

# 4. Same 20 inputs

**Input 1:**

"Data Science Director needed to lead product strategy and analytics vision. Must know Generative ML, Discriminative ML, Contrastive ML, Classification, Gradient Boosting, Causal Inference, AI, and advanced statistics. 8+ years of experience required. Full-time position."

**Input 2:**

"Senior Data Scientist needed to build large-scale semantic analysis and question-answering systems for medical data. Must know NLP, Machine Learning, Deep Learning, LLMs, Transformers, Information Extraction, NER, Entity Linking, and Q&A. 5+ years of experience required."

**Input 3:**

"Staff Data Scientist needed to drive business growth through data analysis, forecasting, and predictive modeling. Must know SQL, Python or R, statistical methods, and machine learning. Full-time position."

**Input 4:**

"Senior Staff Data Scientist needed to solve complex product and engineering problems using quantitative modeling and experimentation. Must know Machine Learning, Deep Learning, Statistical Modeling, Forecasting, Econometrics, PyTorch, TensorFlow, scikit-learn, SQL, Python, and R. 7+ years of experience required."

**Input 5:**

"Staff Data Scientist needed for a Growth team to analyze web-scale data and solve product and business problems. Must know Python, R, SQL, Hive, experimentation design, experimentation analysis, metrics definition, and data pipeline prototyping. Full-time remote position."

**Input 6:**

"Staff Data Scientist needed for a Browse Discovery team to improve user-facing and business-facing products. Must know data analysis, quantitative modeling, Machine Learning, statistical modeling, forecasting, econometrics, PyTorch, TensorFlow, scikit-learn, SQL, Python, and R. 6+ years of experience required."

**Input 7:**

"Senior Data Scientist needed for a Search team to develop product solutions using quantitative modeling and algorithms. Must know Machine Learning, statistical modeling, forecasting, econometrics, PyTorch, TensorFlow, scikit-learn, SQL, Python, R, and experimentation. Full-time position."

**Input 8:**

"Senior Data Scientist needed for a Growth team to apply scientific methods and machine learning to product development. Must know data analysis, Machine Learning, statistical modeling, forecasting, econometrics, PyTorch, TensorFlow, scikit-learn, SQL, Python, and R. 4+ years of experience required."

**Input 9:**

"Senior Data Scientist needed to develop and deploy machine learning features across multiple products. Must have strong knowledge of computer vision, NLP, Deep Learning, ML algorithms, Python, and Large Language Models. Mentoring experience required. Full-time remote position."

**Input 10:**

"Lead Data Scientist needed to build and deploy machine learning solutions at scale. Must know data analysis, data mining, optimization, clustering, regression, classification, statistical inference, predictive modeling, algorithms, data structures, and software development. 6+ years of experience required."

**Input 11:**

"Data Scientist needed to extract insights from high-volume, high-dimensional datasets. Must know advanced statistical analysis, algorithms, predictive modeling, experimentation, pattern recognition, AI, Deep Learning, data structures, distributed systems, and software development. Full-time position."

**Input 12:**

"Cybersecurity Data Scientist Manager needed to lead data science and engineering teams developing security analytics solutions. Must know Python, Databricks, Spark, microservices, cybersecurity datasets, machine learning, data parsing and cleansing, GitHub, Jira, and Agile Scrum. 8+ years of experience required. On-site position."

**Input 13:**

"Senior Data Scientist needed to build credit and fraud machine learning models from feature engineering through production and monitoring. Must know Machine Learning, PySpark, and A/B testing. Full-time remote position."

**Input 14:**

"Senior NLP Data Scientist needed to develop AI-powered legal and contract management products. Must know Machine Learning, Deep Learning, NLP, RNNs, CNNs, Transformers, NER, Q&A, Python, TensorFlow, PyTorch, Spark, Databricks, and AWS SageMaker. 5+ years of experience required."

**Input 15:**

"Principal Data Scientist needed to lead the development of advanced AI/ML products and machine learning platforms. Must know Machine Learning, NLP, personalization and ranking, Deep Learning, Generative AI, LLMs, MLOps, Python, SQL, Databricks, Snowflake, and Kubernetes. Full-time position."

**Input 16:**

"Senior AI/ML Data Scientist needed to design, build, and deploy data-driven AI/ML solutions. Must know Deep Learning, PyTorch, NLP, Generative AI, Python, SQL, cloud data warehouses, RDBMS, and data wrangling. 5+ years of experience required. Remote position."

**Input 17:**

"Data Scientist needed to develop models for energy-market analytics and clean-tech applications. Must know Classical Machine Learning, Deep Learning, Python, NumPy, Pandas, SciPy, time series modeling, and advanced statistics. Full-time position."

**Input 18:**

"Forecast Analyst needed to manage forecasting and projection models for a retail call center. Must know forecasting, predictive modeling, Machine Learning, advanced statistics, SQL, Python, R, business analysis, Excel, PowerPoint, and workforce management. 3+ years of experience required."

**Input 19:**

"Lead Data Scientist needed to develop analytics solutions for retail pharmacy payer analytics, pricing, reimbursement, and margin optimization. Must know SQL, Python, Machine Learning, optimization, mathematics, statistics, A/B testing, data visualization, and Tableau. Full-time remote position."

**Input 20:**

"Research Scientist needed to conduct independent research on complex machine learning problems and responsible AI. Must have strong knowledge of Machine Learning fundamentals and experience contributing to ML research. 4+ years of experience required. Full-time position."

---

# 5. We need a ground truth

This is one of the most important parts of the assignment.

We cannot simply say:

"Prompt 4 looks better."

We need to define what the correct answer is.

For every input, we should have an expected/correct output.

Example:

Input:

"Backend Developer required with 3 years of Python experience. Experience with FastAPI and PostgreSQL preferred. Remote."

Expected:

{
    "job_title": "Backend Developer",
    "experience_years": 3,
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "work_type": "Remote"
}

This expected answer is called our:

**Ground Truth**

---

# 6. What does "correct" mean?

Before running the experiment, we need to define our scoring rules.

For example, we could score each extracted field separately.

Fields:

- job_title
- experience_years
- skills
- work_type

Suppose the model produces:

{
    "job_title": "Backend Developer",
    "experience_years": 3,
    "skills": ["Python", "FastAPI"],
    "work_type": "Remote"
}

But the ground truth says:

{
    "job_title": "Backend Developer",
    "experience_years": 3,
    "skills": ["Python", "FastAPI", "PostgreSQL"],
    "work_type": "Remote"
}

Then:

job_title → correct
experience_years → correct
skills → partially correct
work_type → correct

This gives us something measurable.

---

# 7. What should we score?

We should measure multiple things.

## A. Accuracy

How often did the model extract the correct information?

Example:

18 correct fields out of 20

Accuracy = 90%

---

## B. JSON / format validity

Especially important for the structured-output prompt.

Example:

20 outputs generated.

19 are valid JSON.

Format validity = 95%

This measures whether the model followed our required structure.

---

## C. Completeness

Did the model extract all required information?

For example:

Expected skills:

["Python", "FastAPI", "PostgreSQL"]

Model:

["Python"]

The output may be valid, but it is incomplete.

---

## D. Overall score

We can combine our measurements into a final score.

For example:

Overall Score =
field accuracy + completeness + format validity

We will decide the exact scoring formula BEFORE running the experiment.

That makes the experiment fair.

---

# 8. Why scoring is important

Imagine we get these results:

| Prompt | Accuracy |
|---|---:|
| Naive | 72% |
| Few-shot | 84% |
| Chain-of-thought | 81% |
| Structured | 94% |

Now we have evidence.

We can say:

> Structured-output prompting performed best on this task, achieving 94% accuracy compared with 72% for the naive prompt.

That's much stronger than simply saying:

> "Structured prompting is better."

---

# 9. The CLI tool

The assignment specifically asks for a small CLI tool.

So eventually we should be able to run something like:

python main.py

or something similar.

The CLI should:

1. Load the 20 test inputs.
2. Load the four prompt files.
3. Send each input through each prompt.
4. Collect the model responses.
5. Compare responses with the ground truth.
6. Calculate scores.
7. Save/display the results.

Conceptually:

                            20 Inputs
                                |
          +-------------+---------------------------+
          |             |             |             |
       Naive        Few-shot          CoT       Structured
          |             |             |             |
          +-------------+-------------+-------------+
                                |
                              Results
                                |
                              Scoring
                                |
                            Comparison
                                |
                           Final Winner


# 10. Prompt files

The assignment specifically says:

> Prompts stored in version-controlled files, not inline strings.

This means we should NOT do this:

prompt = """
You are an AI...
"""

inside our Python code.

Instead, we should have something like:

prompts/
    naive.txt
    few_shot.txt
    chain_of_thought.txt
    structured.txt

Then Python loads these files.

This makes the prompts easy to:

- edit
- compare
- version
- track with Git

This directly applies the lesson:

> Treat prompts like code.

---

# 11. Dataset / test data

We will need:

20 inputs

and their:

20 expected outputs / ground truths.

Something like:

data/
    inputs.json
    ground_truth.json

Or we can keep them together:

data/
    test_cases.json

Each test case could conceptually contain:

{
    "input": "...",
    "expected": {
        ...
    }
}

This will make automated evaluation easier.

---

# 12. Expected project structure

The final project could look approximately like this:

prompt-lab/
│
├── prompts/
│   ├── naive.txt
│   ├── few_shot.txt
│   ├── chain_of_thought.txt
│   └── structured.txt
│
├── data/
│   └── test_cases.json
│
├── results/
│   └── results.json
│
├── src/
│   ├── main.py
│   ├── llm.py
│   └── evaluator.py
│
├── README.md
├── requirements.txt
└── .gitignore


# 13. Written comparison

The second part of the assignment is the written comparison.

After running the experiment, we should explain:

## 1. What task did we choose?

Example:

"Extract structured job information from unstructured job descriptions."

## 2. What were the four prompts?

Explain:

- Naive
- Few-shot
- Chain-of-thought
- Structured-output

## 3. How did we evaluate them?

Explain:

- Ground truth
- Field-level accuracy
- Completeness
- Format validity
- Overall score

## 4. What were the results?

Example:

| Prompt | Accuracy | Format Validity | Overall |
|---|---:|---:|---:|
| Naive | 72% | 90% | 75% |
| Few-shot | 84% | 94% | 85% |
| CoT | 81% | 92% | 82% |
| Structured | 94% | 100% | 95% |

These numbers are just examples.

We will calculate the REAL numbers from our experiment.

## 5. Which prompt won?

We will identify the highest-scoring prompt.

## 6. Why did it win?

We should explain based on the results.

For example:

"Structured-output prompting performed best because the task required extracting multiple fields into a predictable format. The strict schema reduced missing fields and formatting errors."


# 14. What this project demonstrates

This small project actually covers many things you learned this week.

### Tokens

The prompts and inputs become tokens before the model processes them.

### Next-token prediction

The model generates the output token by token.

### Context window

The prompt + examples + input + output all consume context.

### Message roles

We can use:

System → instructions

User → input

Assistant → response

### Zero-shot

Our naive prompt can represent zero-shot prompting.

### Few-shot

Our second prompt gives examples.

### Chain-of-thought / reasoning

Our third prompt tests whether explicit reasoning steps help.

### Structured output

Our fourth prompt enforces a predictable format.

### Prompt versioning

Prompts live in separate files and can be tracked with Git.

### Prompt testing

Our 20 inputs become the test set.

### Evaluation

We define correctness and calculate scores.

So the project is basically:

Prompt Engineering
        +
Experimentation
        +
Evaluation
        +
CLI
        +
Version Control


# 15. Important principle

The most important idea of this project is:

> We are not trying to prove that one prompting technique is always better.

We are testing:

> Which prompting technique works best for OUR chosen task and OUR test dataset?

For example, structured output may win for information extraction.

But that does not mean structured output will always beat few-shot prompting for every possible task.

The experiment should be based on evidence.

---

# 16. How we will build it together

We should NOT jump directly into coding.

I suggest we follow this order:

Step 1 → Understand the assignment
        ↓
Step 2 → Choose the task
        ↓
Step 3 → Decide the input data
        ↓
Step 4 → Define the expected output / ground truth
        ↓
Step 5 → Define what "correct" means
        ↓
Step 6 → Design the scoring system
        ↓
Step 7 → Design the four prompts
        ↓
Step 8 → Decide the LLM/API to use
        ↓
Step 9 → Create project structure
        ↓
Step 10 → Implement the CLI
        ↓
Step 11 → Run all 20 × 4 experiments
        ↓
Step 12 → Calculate scores
        ↓
Step 13 → Compare results
        ↓
Step 14 → Write the final report
        ↓
Step 15 → Put everything under Git/version control


# 17. One important calculation

We have:

20 inputs

and:

4 prompts

Therefore:

20 × 4 = 80 model evaluations

So our experiment will generate approximately:

80 model responses

Then we evaluate those 80 responses.

This is why we need automation instead of manually testing everything.


# 18. What I recommend we decide first

Before writing any code, we should answer these questions:

1. What task are we going to test?

2. What will each input look like?

3. What information should the model extract/generate?

4. What should the correct output look like?

5. How will we create the 20 test cases?

6. How will we score correctness?

7. Which LLM/API will we use?

Once these are decided, the implementation becomes much easier.


# Current status

We are currently at:

[DISCUSSION / PLANNING]

We have NOT started implementation yet.

The first actual decision we need to make is:

> **Which task should we choose for the Prompt Lab?**

My recommendation is to choose a task that is:
- easy to understand
- easy to create 20 test cases for
- easy to define ground truth for
- easy to score automatically
- clearly shows differences between prompting techniques

A structured information-extraction task is a very good choice for this assignment.