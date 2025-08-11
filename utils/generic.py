import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from utils.yelp_business_fetch import restaurant_search
from utils.the_movie_db_fetch import get_movie_recommendations


class State(TypedDict):
    messages: Annotated[list, add_messages]


def load_prompt_from_file(file_path: str) -> str:
    """Load a prompt from a text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def init_and_load_env():
    load_dotenv()  # Load variables from .env

    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    os.environ["YELP_API_KEY"] = os.getenv("YELP_API_KEY")
    os.environ["THE_MOVIE_DB_API_KEY"] = os.getenv("THE_MOVIE_DB_API_KEY")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("Google API key is not set in environment variables.")

    yelp_api_key = os.getenv("YELP_API_KEY")
    if not yelp_api_key:
        raise ValueError("Yelp API key is not set in environment variables.")

    the_movie_db_api_key = os.getenv("THE_MOVIE_DB_API_KEY")
    if not the_movie_db_api_key:
        raise ValueError("TMDB API key is not set in environment variables.")

    # Initialize Google Generative AI client
    llm = ChatGoogleGenerativeAI(
        api_key=google_api_key,
        model="gemini-2.5-flash",
        temperature=0.3,
        max_tokens=1000,
        convert_system_message_to_human=True,
    )

    tools = [restaurant_search, get_movie_recommendations]

    llm_with_tools = llm.bind_tools(tools=tools)

    # Node definition for the tool invocation
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # Build the graph
    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_node("tools", ToolNode(tools=tools))

    ## adding edges
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")
    builder.add_edge("chatbot", END)

    graph = builder.compile()

    # Get the PNG bytes from the Mermaid graph
    png_bytes = graph.get_graph().draw_mermaid_png()

    # Save to file
    with open(r"./static/chatbot_lang_graph.png", "wb") as f:
        f.write(png_bytes)
    
    return graph
