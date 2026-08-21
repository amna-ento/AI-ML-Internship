from pathlib import Path


def search_file(query):

    file_path = Path(__file__).parent / "job_description.txt"

    with open(file_path, "r") as file:
        content = file.read()

    query = query.lower()

    if "skill" in query:
        start = content.find("Required Skills:")
        end = content.find("Work Type:")

        if start != -1 and end != -1:
            return content[start:end].strip()

    elif "experience" in query:
        start = content.find("experience")
        end = content.find("Required Skills:")

        if start != -1 and end != -1:
            return content[start:end].strip()

    elif "work type" in query or "remote" in query:
        start = content.find("Work Type:")
        end = content.find("Education:")

        if start != -1 and end != -1:
            return content[start:end].strip()

    elif "education" in query or "degree" in query:
        start = content.find("Education:")

        if start != -1:
            return content[start:].strip()

    return "No relevant information found."


tools = [
    {
        "name": "search_file",
        "description": "Search the job description and return only the information relevant to the user's question.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's question about the job"
                }
            },
            "required": ["query"]
        }
    }
]


user_query = input("Ask something about the job: ")

print("\nUser:", user_query)

tool_call = {
    "name": "search_file",
    "arguments": {
        "query": user_query
    }
}

print("\nLLM selected tool:", tool_call["name"])

if tool_call["name"] == "search_file":
    result = search_file(
        tool_call["arguments"]["query"]
    )
else:
    result = "Unknown tool"

print("\nAnswer:")
print(result)
