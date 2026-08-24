def stream_response(response):

    full_response = ""

    for chunk in response:

        if chunk.choices:

            content = chunk.choices[0].delta.content

            if content:
                print(
                    content,
                    end="",
                    flush=True
                )

                full_response += content

    print()

    return full_response