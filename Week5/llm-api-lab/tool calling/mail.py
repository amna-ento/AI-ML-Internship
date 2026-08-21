import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


emails = [
    {
        "id": 1,
        "sender": "hr@company.com",
        "subject": "Interview Schedule",
        "body": "Your interview is scheduled for Monday at 10 AM."
    },
    {
        "id": 2,
        "sender": "manager@company.com",
        "subject": "Project Update",
        "body": "Please submit the project by Friday."
    },
    {
        "id": 3,
        "sender": "hr@company.com",
        "subject": "Company Policy",
        "body": "Please review the updated company policy."
    }
]


def search_emails(query):
    results = []

    for email in emails:
        if (
            query.lower() in email["sender"].lower()
            or query.lower() in email["subject"].lower()
            or query.lower() in email["body"].lower()
        ):
            results.append(email)

    if not results:
        return "No emails found."

    return json.dumps(results)


def read_email(email_id):
    for email in emails:
        if email["id"] == email_id:
            return json.dumps(email)

    return "Email not found."


def send_email(to, subject, body):
    new_email = {
        "id": len(emails) + 1,
        "sender": "me@company.com",
        "subject": subject,
        "body": body
    }

    emails.append(new_email)

    return f"Email sent successfully to {to}."


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_emails",
            "description": "Search emails by sender, subject, or content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for in emails."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Read a specific email using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {
                        "type": "integer",
                        "description": "The ID of the email to read."
                    }
                },
                "required": ["email_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address."
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject."
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body."
                    }
                },
                "required": ["to", "subject", "body"]
            }
        }
    }
]


messages = [
    {
        "role": "system",
        "content": "You are an email assistant. Use email tools when needed. If no tool is needed, answer normally."
    }
]


messages = [
    {
        "role": "system",
        "content": "You are an email assistant. Use email tools when needed. If no tool is needed, answer normally and only provide information relevant to the user's question."
    }
]


while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Conversation ended.")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    while True:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            answer = message.content
            print("Assistant:", answer)

            messages.append({
                "role": "assistant",
                "content": answer
            })

            break

        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in message.tool_calls
            ]
        })

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if tool_name == "search_emails":

                result = search_emails(
                    arguments["query"]
                )

            elif tool_name == "read_email":

                result = read_email(
                    arguments["email_id"]
                )

            elif tool_name == "send_email":

                result = send_email(
                    arguments["to"],
                    arguments["subject"],
                    arguments["body"]
                )

            else:

                result = "Unknown tool."

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })