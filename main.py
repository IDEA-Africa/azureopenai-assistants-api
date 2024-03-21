# main.py
# from assistant_initialization import assistant
# from assistant_initialization import system_prompt
from assistant_initialization import assistant, system_prompt

from assistant_cli.assistant import AssistantCLI
import config

thread_id = config.assistant_thread_id



# def bing_search_wrapper(query: str, count: int = 5) -> str:
#     """Function wrapper to perform a Bing search and format the results."""
#     results = bing_search_service.perform_custom_bing_search(query, count)
#     formatted_results = [{"title": res["title"], "url": res["link"], "snippet": res["snippet"]} for res in results]
#     # Format the results as needed. Here, just converting it to a simple list of titles for simplicity.
#     return "\n".join([f"Title: {res['title']}, URL: {res['url']}" for res in formatted_results])



# handle Bing Search Service
def _handle_tool_call(self, required_actions):
    """
    Handle tool calls made by the OpenAI Assistant.

    This needs to correctly call the BingSearchService when required.
    """
    tool_outputs = []
    for action in required_actions["tool_calls"]:
        func_name = action['function']['name']
        arguments = json.loads(action['function']['arguments'])

        if func_name == "perform_custom_bing_search":
            # Assuming `arguments` is a dict with correct keys for `perform_custom_bing_search`
            output = BingSearchService().perform_custom_bing_search(**arguments)
            # Format output as needed
            tool_outputs.append({"tool_call_id": action['id'], "output": output})
        else:
            # Handle other functions
            pass
    return tool_outputs


# def ask_assistant(query=None):
#     response = assistant.get_assistant_response(
#         thread_id=thread_id,
#         instructions=system_prompt,
#         user_message=query,
#     )
#     return response.data[0].content[0].text.value

# def ask_assistant(query=None):
#     """Function to interact with the assistant and get responses."""
#     response = assistant.get_assistant_response(
#         instructions=system_prompt,
#         user_message=query,
#         thread_id=thread_id
#     )
#     return response

def ask_assistant(query: str) -> str:
    """
    Sends a query to the assistant and processes the response.
    """
    response = assistant.get_assistant_response(
        instructions=system_prompt,
        user_message=query,
        thread_id=thread_id  # Make sure thread_id is correctly initialized
    )
    # Process and format the response appropriately
    return response



# if __name__ == "__main__":
#     ai_interface = AssistantCLI(response_handler=ask_assistant)
#     ai_interface.run()

# if __name__ == "__main__":
#     query = input("Ask the assistant: ")
#     response = ask_assistant(query=query)
#     print("Assistant's response:")
#     print(response)


if __name__ == "__main__":
    query = input("Ask the assistant: ")
    # query = "What is the capital of Japan?"
    response = ask_assistant(query)
    print(response)