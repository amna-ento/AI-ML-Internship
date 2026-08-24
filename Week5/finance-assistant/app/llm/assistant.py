from app.llm.client import client
from app.llm.tool_definitions import TOOL_DEFINITIONS
from app.llm.tool_executor import execute_tool
from app.llm.conversation import Conversation
from app.llm.streaming import stream_response
from app.utils.retry import call_groq
from app.utils.usage import log_usage
from app.utils.errors import handle_error


def ask_llm(
    user_message,
    conversation
):

    try:

        conversation.add_user_message(
            user_message
        )

        messages = conversation.get_messages()

        # Ask Groq what to do
        response = call_groq(
            client,
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto"
        )

        # Log usage
        if response.usage:

            log_usage(
                "openai/gpt-oss-20b",
                response.usage
            )

        message = response.choices[0].message

        # No tool is needed
        if not message.tool_calls:

            stream = call_groq(
                client,
                model="openai/gpt-oss-20b",
                messages=messages,
                stream=True
            )

            print(
                "\nAssistant: ",
                end="",
                flush=True
            )

            final_message = stream_response(
                stream
            )

            conversation.add_assistant_message(
                final_message
            )

            return final_message

        # Add assistant's tool request
        messages.append(message)

        # Execute requested tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            result = execute_tool(
                tool_name,
                arguments
            )

            # Add tool result
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

        # Ask Groq for final response
        final_response = call_groq(
            client,
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            stream=True
        )

        print(
            "\nAssistant: ",
            end="",
            flush=True
        )

        final_message = stream_response(
            final_response
        )

        conversation.add_assistant_message(
            final_message
        )

        return final_message

    except Exception as error:

        # Convert technical error
        # into a user-friendly message
        friendly_message = handle_error(
            error
        )

        print(
            "\nAssistant:",
            friendly_message
        )

        return friendly_message