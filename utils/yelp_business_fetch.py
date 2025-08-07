import os

import requests
from dotenv import load_dotenv
from langchain.tools import tool
from pydantic import BaseModel, Field


def get_yelp_cache_data(api_key_arg=None, base_url_arg=None, timeout_arg=None):
    """Get cached Yelp API configuration data."""
    load_dotenv()  # Load variables from .env

    api_key = api_key_arg or os.getenv("YELP_API_KEY")
    if not api_key:
        raise ValueError("Yelp API key is not set in environment variables.")

    price_tiers = {
        "cheap": "1",
        "moderate": "2",
        "expensive": "3",
        "very expensive": "4",
    }

    base_url = base_url_arg or "https://api.yelp.com/v3/businesses/search"
    if not base_url:
        raise ValueError("Yelp API base URL is not set in environment variables.")

    timeout = timeout_arg or 10
    return api_key, base_url, price_tiers, timeout


class RestaurantSearchToolInput(BaseModel):
    """Input schema for restaurant search tool."""

    cuisine: str = Field(
        ...,
        description="Search cuisine for the restaurant, e.g., 'japanese', 'indian', 'italian', 'mexican'.",
    )
    location: str = Field(
        ...,
        description="Location to search for restaurants, e.g., 'San Francisco, CA'.",
    )
    price_tiers: str = Field(
        ...,
        description="Price tier for the restaurant. Options are 'cheap', 'moderate', 'expensive', 'very expensive'.",
    )
    limit: int = Field(
        default=5,  # Changed from 3 to match function default
        description="Number of results to return (1-50).",
    )


@tool(args_schema=RestaurantSearchToolInput)
def restaurant_search(cuisine, location, price_tiers, limit=5):
    """Search for restaurants using the Yelp API based on specified criteria.

    This function queries the Yelp API to find restaurants that match the given
    search parameters including search cuisine, location, price range, and result limit.

    Args:
        cuisine (str): The search cuisine to look for restaurants (e.g., 'japanese', 'indian',
                      'italian', 'mexican'). This is used to filter businesses by category,
                      name, or cuisine type.
        location (str): The geographic location to search in. Can be a city name,
                       address, zip code, or coordinates (e.g., "New York, NY",
                       "10001", "Times Square").
        price_tiers (str): The price tier preference for restaurants. Should be a key that
                    maps to Yelp's price scale in the price_tiers configuration.
                    Options: 'cheap', 'moderate', 'expensive', 'very expensive'
        limit (int, optional): Maximum number of restaurant results to return.
                              Defaults to 5. Maximum allowed by Yelp API is typically 50.

    Returns:
        list[dict]: A list of restaurant business objects from Yelp API. Each dictionary
                   contains restaurant details such as:
                   - name: Restaurant name
                   - rating: Average rating
                   - price: Price tier
                   - location: Address information
                   - phone: Contact number
                   - url: Yelp page URL
                   - categories: List of cuisine/category types
                   Returns empty list if no businesses are found.
    """
    api_key, base_url, price_tiers_mpping, timeout = get_yelp_cache_data()

    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "cuisine": cuisine,
        "location": location,
        "limit": limit,
        "price_tiers": price_tiers_mpping.get(
            price_tiers, "2"
        ),  # Changed default from "3" to "2" (moderate)
    }

    response = requests.get(base_url, headers=headers, params=params, timeout=timeout)

    if response.status_code != requests.codes.ok:
        raise Exception(
            f"Error fetching data from Yelp API: {response.status_code} - {response.text}"
        )

    response.raise_for_status()
    return response.json().get("businesses", [])
