import os
import time
import random
import requests
from dotenv import load_dotenv
from langchain.tools import tool 
from pydantic import BaseModel, Field

class MovieRecommendationToolInput(BaseModel):
    movie_title: str = Field(
        ...,
        description="The title of the movie to search and provide recommendations.",
    )

def get_the_movie_db_cache_data(the_movie_db_api_key_arg = None, base_url_arg = None):
    """
    Get TMDB API cache data.
    """
    the_movie_db_api_key = the_movie_db_api_key_arg or os.getenv("THE_MOVIE_DB_API_KEY")
    if not the_movie_db_api_key:
        raise ValueError("TMDB API key is not set in environment variables.")
    
    base_url = base_url_arg or os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("TMDB API base URL is not set in environment variables.")
    
    return base_url, the_movie_db_api_key
    

def make_request_with_retry(url, params, headers, max_retries=105, min_wait=10, max_wait=20):
    response = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit exceeded
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = random.randint(min_wait, max_wait)
                print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print(f"Error: Status {response.status_code} on {url}: {response.text}")
                break  # Break out for other errors
        except Exception as e:
            wait_time = random.randint(min_wait, max_wait)
            print(f"Rate limit hit. Waiting {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        
    return None


@tool(args_schema=MovieRecommendationToolInput)
def get_movie_recommendations(movie_title: str) -> dict:
    """
    Search for a movie on The Movie Database (TMDB) by title, retrieve its unique movie ID, 
    then fetch and return a list of recommended movies with basic details.

    This tool performs a two-step process:
    1. **Movie Search** — Uses the `/search/movie` endpoint to find the first matching movie 
       and extract its TMDB movie ID.
    2. **Recommendations Retrieval** — Uses the `/movie/{movie_id}/recommendations` endpoint 
       to get movies that TMDB recommends based on similarity to the found movie.

    Args:
        movie_title (str):
            The title of the movie to search for. Example: "Inception".
            Partial titles and case-insensitive matches are supported.

    Returns:
        dict: 
            A dictionary containing:
            - **found_title** (str | None): 
                The exact movie title found on TMDB, or `None` if no match is found.
            - **recommendations** (list[dict]):
                A list of recommended movies, each containing:
                - `title` (str): Movie title.
                - `rating` (float | "N/A"): Average TMDB user rating (0–10 scale).
                - `language` (str | "N/A"): ISO 639-1 language code (e.g., "en", "fr").
                - `poster-img` (str | "N/A"): Movie poster image if available.

    Example:
        >>> get_movie_recommendations("Inception")
        {
            "found_title": "Inception",
            "recommendations": [
                {
                    "title": "The Prestige",
                    "rating": 8.2,
                    "language": "en",
                    "poster-img": "https://image.tmdb.org/t/p/original/abc.jpg"
                },
                {
                    "title": "Interstellar",
                    "rating": 8.4,
                    "language": "en",
                    "poster-img": https://image.tmdb.org/t/p/original/abc123.jpg,
                }
            ]
        }

    Notes:
        - This function requires a valid TMDB API key set in environment variables 
          or retrieved from `get_the_movie_db_cache_data()`.
        - Only the first search result is used for recommendations.
        - For full director and cast information, see TMDB's `/credits` endpoint.
    """
    load_dotenv()

    tmdb_base_url, the_movie_db_api_key = get_the_movie_db_cache_data()
    search_url = f"{tmdb_base_url}/search/movie"
    search_params = {"query": movie_title}
    headers = {"Authorization": f"Bearer {the_movie_db_api_key}"}

    # Step 1: Find movie ID
    search_resp = make_request_with_retry(search_url, search_params, headers)
    if not search_resp or not search_resp.get("results"):
        return {"found_title": None, "recommendations": []}

    movie_id = search_resp["results"][0]["id"]
    found_title = search_resp["results"][0]["title"]

    # Step 2: Get recommendations
    rec_url = f"{tmdb_base_url}/movie/{movie_id}/recommendations"
    rec_params = {"language": "en-US", "page": 1}
    print(f"Fetching recommendations for movie ID: {movie_id} ({found_title})")
    print(f"Requesting URL: {rec_url} with params: {rec_params}")
    rec_resp = make_request_with_retry(rec_url, rec_params, headers)

    if not rec_resp:
        return {"found_title": found_title, "recommendations": []}

    print(f"Recommendations response for movie '{found_title}': {rec_resp}")
    recommendations = []
    for movie in rec_resp.get("results", []):
        recommendations.append({
            "title": movie["title"],
            "rating": movie.get("vote_average", "N/A"),
            "language": movie.get("original_language", "N/A"),
            "poster-img": r'https://image.tmdb.org/t/p/original/' + movie.get("poster_path", "N/A")
        })

    return {"found_title": found_title, "recommendations": recommendations}

if __name__ == "__main__":
    print(get_movie_recommendations("Inception"))