import json
import logging
import os
import time

from dotenv import load_dotenv
from groq import Groq
from groq import RateLimitError, APITimeoutError, APIConnectionError, APIStatusError

from app.models import FinanceResponse
from app.tools import calculator, currency_converter, get_expenses


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

MAX_RETRIES = 3
MAX_TOOL_ROUNDS = 5

INPUT_COST_PER_MILLION = 0.15
OUTPUT_COST_PER_MILLION = 0.60

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are a personal finance assistant.

You help users with:
- calculations
- currency conversion
- expense analysis
- expense management suggestions

Use the available tools whenever actual calculations, current exchange
rates, or database information are required.

Never invent expense data or exchange rates.

You decide which tool to use based on the user's request.

After receiving tool results, answer the user clearly and concisely.

And one most important thing you are bound to reply finance or calculation, currency exchange, expense analysis, expense managment, or finance related questions
 if the user ask for an irrelevent question simple reply: "I'm a personal finance assistant, so ask me queries related to that"
 
 and be a calm humble assistant like for ok, nice, or any remark or general thing like that just say: "if you have any other query related to finance do let me lnow"
"""


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform basic arithmetic calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A basic arithmetic expression."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "currency_converter",
            "description": "Convert money between currencies using current exchange rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number"
                    },
                    "from_currency": {
                        "type": "string"
                    },
                    "to_currency": {
                        "type": "string"
                    }
                },
                "required": [
                    "amount",
                    "from_currency",
                    "to_currency"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_expenses",
            "description": "Retrieve expenses from the local finance database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": ["string", "null"],
                        "description": "Optional expense category. Use null when no category is specified."
                    }
                },
                "required": []
            }
        }
    }
]


AVAILABLE_TOOLS = {
    "calculator": calculator,
    "currency_converter": currency_converter,
    "get_expenses": get_expenses
}


def call_with_retry(messages):
    for attempt in range(MAX_RETRIES):
        try:
            return client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                temperature=0.2,
                max_completion_tokens=1000
            )

        except (RateLimitError, APITimeoutError, APIConnectionError) as error:
            if attempt == MAX_RETRIES - 1:
                raise

            wait_time = 2 ** attempt

            logger.warning(
                "Transient LLM error: %s. Retry %s/%s in %s seconds.",
                error,
                attempt + 1,
                MAX_RETRIES,
                wait_time
            )

            time.sleep(wait_time)

        except APIStatusError as error:
            if error.status_code >= 500 and attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt

                logger.warning(
                    "Server error: %s. Retry %s/%s in %s seconds.",
                    error,
                    attempt + 1,
                    MAX_RETRIES,
                    wait_time
                )

                time.sleep(wait_time)
                continue

            raise


def execute_tool(tool_name, arguments):
    tool = AVAILABLE_TOOLS.get(tool_name)

    if not tool:
        return {
            "success": False,
            "tool": tool_name,
            "data": {},
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        if tool_name == "get_expenses" and arguments.get("category") is None:
            arguments.pop("category", None)

        result = tool(**arguments)
        return result.model_dump()

    except Exception as error:
        logger.exception("Tool execution failed: %s", tool_name)

        return {
            "success": False,
            "tool": tool_name,
            "data": {},
            "error": str(error)
        }

def extract_usage(response):
    usage = getattr(response, "usage", None)

    if not usage:
        return {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }

    return {
        "input_tokens": getattr(usage, "prompt_tokens", 0),
        "output_tokens": getattr(usage, "completion_tokens", 0),
        "total_tokens": getattr(usage, "total_tokens", 0)
    }


def add_usage(total_usage, usage):
    for key in total_usage:
        total_usage[key] += usage.get(key, 0)


def estimate_cost(usage):
    input_cost = (
        usage["input_tokens"]
        / 1_000_000
        * INPUT_COST_PER_MILLION
    )

    output_cost = (
        usage["output_tokens"]
        / 1_000_000
        * OUTPUT_COST_PER_MILLION
    )

    return round(input_cost + output_cost, 8)


def log_usage(usage):
    cost = estimate_cost(usage)

    logger.info(
        "LLM usage | input=%s output=%s total=%s estimated_cost=$%s",
        usage["input_tokens"],
        usage["output_tokens"],
        usage["total_tokens"],
        cost
    )

    return cost


def parse_final_response(content, tools_used, data):
    return FinanceResponse(
        answer=content,
        tool_used=tools_used,
        status="success",
        data=data
    )


def run_finance_assistant(user_input):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    tools_used = []

    total_usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }

    tool_data = {}

    for _ in range(MAX_TOOL_ROUNDS):
        response = call_with_retry(messages)

        usage = extract_usage(response)
        add_usage(total_usage, usage)

        message = response.choices[0].message

        if not message.tool_calls:
            cost = log_usage(total_usage)

            return parse_final_response(
                message.content or "",
                tools_used,
                {
                    "tool_results": tool_data,
                    "usage": total_usage,
                    "estimated_cost": cost
                }
            )

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError:
                arguments = {}

            tools_used.append(tool_name)

            tool_result = execute_tool(
                tool_name,
                arguments
            )

            tool_data[tool_name] = tool_result

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_result)
                }
            )

    cost = estimate_cost(total_usage)

    return FinanceResponse(
        answer="I could not complete the request.",
        tool_used=tools_used,
        status="error",
        data={
            "tool_results": tool_data,
            "usage": total_usage,
            "estimated_cost": cost
        }
    )


def stream_response(response):
    for word in response.answer.split():
        yield word + " "
        
        
        
def stream_finance_assistant(user_input):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    tools_used = []

    total_usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }

    tool_data = {}

    for _ in range(MAX_TOOL_ROUNDS):
        response = call_with_retry(messages)

        usage = extract_usage(response)
        add_usage(total_usage, usage)

        message = response.choices[0].message

        if not message.tool_calls:
            final_prompt = messages + [
                {
                    "role": "assistant",
                    "content": message.content or ""
                }
            ]

            stream = client.chat.completions.create(
                model=MODEL,
                messages=final_prompt,
                temperature=0.2,
                max_completion_tokens=1000,
                stream=True
            )

            full_response = ""

            for chunk in stream:
                content = chunk.choices[0].delta.content

                if content:
                    full_response += content
                    yield {
                        "type": "text",
                        "content": content
                    }

            cost = log_usage(total_usage)

            result = FinanceResponse(
                answer=full_response,
                tool_used=tools_used,
                status="success",
                data={
                    "tool_results": tool_data,
                    "usage": total_usage,
                    "estimated_cost": cost
                }
            )

            yield {
                "type": "complete",
                "result": result
            }

            return

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )
            except json.JSONDecodeError:
                arguments = {}

            tools_used.append(tool_name)

            tool_result = execute_tool(
                tool_name,
                arguments
            )

            tool_data[tool_name] = tool_result

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_result)
                }
            )

    yield {
        "type": "complete",
        "result": FinanceResponse(
            answer="I could not complete the request.",
            tool_used=tools_used,
            status="error",
            data={
                "tool_results": tool_data,
                "usage": total_usage,
                "estimated_cost": estimate_cost(total_usage)
            }
        )
    }        