# assistant_initialization.py

from core.assistant import AssistantManager
import config
import logging
import os

# Ensure to load environment variables if not done elsewhere in your application
from dotenv import load_dotenv
load_dotenv()


# import functions.weather as weather
# import functions.web_browsing as browser

from functions.bing_search import BingSearchService # import the BingSearchService class from the bing_search module
bing_search_service = BingSearchService(bing_search_key=os.getenv("BING_SUBSCRIPTION_KEY"))


log_level = getattr(logging, config.log_level.upper(), "WARNING")
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logging = logging.getLogger(__name__)

system_prompt = """You are an AI financial data analyst assistant for the GCF with access to websearch and server functions. Your purpose is to help employees answer questions and get data insights from provided data and from funtions such as the custom Bing search. You have access to query the web using Bing Search. You should call Bing search whenever a question requires up-to-date information or could benefit from web data.

The websearch function empowers you for real-time web search and information retrieval, particularly for current and relevant data from the internet in response to user queries, especially when such information is beyond your training data or when up-to-date information is essential. Always include the source URL for information fetched from the web.

The functions enables you to fetch up-to-date information from the web about finacial analysis, organizations, sustainable development projects, funding and guarantees, organization's credit scoring, and other related topics. 

All your responses should be in a human-readable format. If possible, include the source URL for information fetched.
"""

thread_id = config.assistant_thread_id

# Make sure your environment variables are correctly set in the .env file or in your environment
api_key = os.getenv("AZURE_OPENAI_API_KEY")
# azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")# picking incorrect endpoint 
azure_endpoint = "https://gcfgenai2oai2.openai.azure.com"
api_version = "2024-02-15-preview"  # Ensure this is correct
assistant_id = os.getenv("AZURE_OPENAI_ASSISTANT_ID")

# Initialize Bing Search Service with API key
bing_search_service = BingSearchService(bing_search_key=os.getenv("BING_SUBSCRIPTION_KEY"))

# # changed the client library from openai to use azureOpenai
# assistant = AssistantManager(
#     # previous
#     # api_key=config.openai_api_key,
#     # assistant_id=config.openai_assistant_id,
    
#     # new azureOpenai
#     api_key=api_key,
#     azure_endpoint=azure_endpoint,
#     api_version=api_version,
#     model="gpt-4",
#     assistant_id=assistant_id,  
#     functions=[
#         # weather.get_weather,
#         # browser.text_search,
#         # kubernetes_changelog.query_by_version,
#         # get_latest_version,
#         # get_release_notes
#         # add the perform_custom_bing_search function to the list of functions
#         BingSearchService().perform_custom_bing_search
        
#     ]
# )

def bing_search_wrapper(query: str, count: int = 5) -> str:
    """Function wrapper to perform a Bing search and format the results."""
    results = bing_search_service.perform_custom_bing_search(query, count)
    formatted_results = [{"title": res["title"], "url": res["link"], "snippet": res["snippet"]} for res in results]
    # Format the results as needed. Here, just converting it to a simple list of titles for simplicity.
    return "\n".join([f"Title: {res['title']}, URL: {res['url']}" for res in formatted_results])


# When initializing AssistantManager
assistant = AssistantManager(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
    assistant_id=assistant_id,
    model="gpt-4",
    functions=[bing_search_wrapper]  # Add the bing_search_wrapper to the list of callable functions
)
