# functions\bing_search.py

import requests
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# logging.basicConfig(level=logging.DEBUG) # set logging level to DEBUG for development, INFO for production

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG) # set logging.INFO for production
logger.propagate = True

class BingSearchService:
    def __init__(self, bing_search_key: str = None, bing_search_url: str = "https://api.bing.microsoft.com/v7.0/search"):
        # If bing_search_key is not passed, fetch it from environment variables
        self.bing_search_key = bing_search_key if bing_search_key is not None else os.getenv("BING_SUBSCRIPTION_KEY")
        # Use the passed bing_search_url if given, else default to the Bing API URL
        self.bing_search_url = bing_search_url

    def perform_custom_bing_search(self, query: str, count: int = 5):
        """
        Performs a custom Bing search and returns the top `count` results.
        This function is designed to retrive the top search results from Bing search engine based on the search query. We use it to search information from the web that is not in our provided private domain.

        Args:
            query (str): The search query.
            count (int, optional): The number of results to retrieve. Defaults to 5.

        Returns:
            list: A list of dictionaries representing the search results. Each dictionary contains the following keys:
                - title (str): The title of the search result.
                - link (str): The URL of the search result.
                - snippet (str): A snippet of the search result.

        Raises:
            requests.exceptions.RequestException: If there is an error performing the Bing search.
            Exception: If there is an unexpected error.

        """
        # add logging
        # logger = logging.getLogger(__name__)

        headers = {"Ocp-Apim-Subscription-Key": self.bing_search_key}
        params = {
            "q": query,
            "count": count,  # Control the number of results
            "textDecorations": True,
            "textFormat": "HTML"
        }

        try:
            response = requests.get(self.bing_search_url, headers=headers, params=params)
            # add a logger
            logger.info(f"Performing Bing search for query: {query}")

            response.raise_for_status()  # This will raise an HTTPError if the response was an error

            search_results = response.json().get('webPages', {}).get('value', [])
            # Format the search results
            output = [
                {
                    "title": result["name"],
                    "link": result["url"],
                    "snippet": result["snippet"]
                } for result in search_results
            ]
            
            # TODO:  Return the search results in JSON-formatted string containing the title, link, and snippet of each result

            return output

        except requests.exceptions.RequestException as e:
            # Handle request errors (network problems, invalid response, etc.)
            # add a logger
            logger.error(f"Error performing Bing search: {e}")
            print(f"Error performing Bing search: {e}")
            return []

        except Exception as e:
            # Handle other errors
            # add a logger
            logger.error(f"An error occurred: {e}")

            # print(f"An error occurred: {e}")
            return []

# example use
if __name__ == "__main__":
    bing_service = BingSearchService()
    results = bing_service.perform_custom_bing_search("What is the capital of Japan?")
    print(results)