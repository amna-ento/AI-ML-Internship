from app.llm.tool_definitions import TOOL_DEFINITIONS


for tool in TOOL_DEFINITIONS:
    function = tool["function"]

    print(
        function["name"],
        "→",
        function["description"]
    )