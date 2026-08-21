import re


# 1. Define the tools

def calculator(expression):
    if not re.fullmatch(r"[0-9+\-*/%.()\s]+", expression):
        return "Invalid mathematical expression"

    return eval(expression, {"__builtins__": {}}, {})


def get_weather(city):
    weather = {
        "Lahore": "32°C, Sunny",
        "Karachi": "30°C, Cloudy",
        "Islamabad": "28°C, Rainy"
    }

    return weather.get(city.title(), "Weather not available")


def extract_tool_name(user_message):
    """Choose a tool from the user's natural-language request."""
    message = user_message.lower()

    if re.search(r"\b(weather|temperature|forecast|rain|sunny|cloudy)\b", message):
        return "get_weather"

    if (
        re.search(r"\b(calculate|calculator|compute|solve)\b", message)
        or re.search(r"\d+\s*[+\-*/%]\s*\d+", message)
    ):
        return "calculator"

    return "unknown"


def extract_arguments(user_message, tool_name):
    """Extract the arguments needed by the selected tool."""
    if tool_name == "calculator":
        expression = re.search(r"[0-9][0-9+\-*/%.()\s]*", user_message)
        if expression:
            return {"expression": expression.group().strip()}
        return {"expression": ""}

    if tool_name == "get_weather":
        known_cities = ("Lahore", "Karachi", "Islamabad")
        for city in known_cities:
            if re.search(rf"\b{city}\b", user_message, re.IGNORECASE):
                return {"city": city}
        return {"city": ""}

    return {}


#  2. Define tool schemas

tools = [
    {
        "name": "calculator",
        "description": "Perform a mathematical calculation",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get weather information for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
]


def main():
    # 3. User request
    user_message = input("user message: ").strip()

    # 4. Extract the tool and arguments from the user's request
    tool_name = extract_tool_name(user_message)
    arguments = extract_arguments(user_message, tool_name)

    # 5. Execute the selected tool
    if tool_name == "calculator":
        result = calculator(arguments["expression"])
    elif tool_name == "get_weather":
        result = get_weather(arguments["city"])
    else:
        result = "Unknown tool"

    # 6. Return result to the LLM
    print("Selected tool:", tool_name)
    print("Tool result:", result)

    # 7. LLM produces final answer
    print("Final answer: The answer is", result)


if __name__ == "__main__":
    main()