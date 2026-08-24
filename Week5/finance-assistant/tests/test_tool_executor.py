from app.llm.tool_executor import execute_tool


# Test a valid tool call
result = execute_tool(
    "calculate",
    '{"expression": "4500 + 1200"}'
)

print("Valid tool:")
print(result)


# Test an unknown tool
result = execute_tool(
    "unknown_tool",
    '{}'
)

print("\nUnknown tool:")
print(result)


# Test invalid JSON
result = execute_tool(
    "calculate",
    '{"expression": "4500 + 1200"'
)

print("\nInvalid JSON:")
print(result)