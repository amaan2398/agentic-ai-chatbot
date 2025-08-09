import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from utils.yelp_business_fetch import restaurant_search


class DataSummarizationToolInput(BaseModel):
    data: str = Field(
        ...,
        description="Data to be summarized, typically a string containing information about restaurants.",
    )


class State(TypedDict):
    messages: Annotated[list, add_messages]


def load_prompt_from_file(file_path: str) -> str:
    """Load a prompt from a text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def init_and_load_env():
    load_dotenv()  # Load variables from .env

    summary_prompt_path = r"static/prompts/summarizer.txt"
    if not os.path.exists(summary_prompt_path):
        raise FileNotFoundError(f"Prompt file {summary_prompt_path} does not exist.")

    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    os.environ["YELP_API_KEY"] = os.getenv("YELP_API_KEY")

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("Google API key is not set in environment variables.")

    yelp_api_key = os.getenv("YELP_API_KEY")
    if not yelp_api_key:
        raise ValueError("Yelp API key is not set in environment variables.")

    # Initialize Google Generative AI client
    llm = ChatGoogleGenerativeAI(
        api_key=google_api_key,
        model="gemini-2.5-flash",
        temperature=0.3,
        max_tokens=1000,
        convert_system_message_to_human=True,
    )

    @tool(args_schema=DataSummarizationToolInput)
    def summarize_data(data):
        """
        Generate a concise executive-level business summary of provided data using an LLM.

        This function leverages a language model to analyze and summarize data from a senior
        business analyst perspective, producing a strategic, executive-focused summary with
        specific formatting and length constraints.

        Args:
            data (Any): The data to be analyzed and summarized. Can be any format that can
                    be converted to string representation (dict, list, DataFrame, JSON, etc.).
                    The data will be embedded directly into the LLM prompt for analysis.

        Returns:
            str: A concise business summary in markdown format, limited to 30 words maximum.
                The response includes:
                - Strategic executive-level analysis
                - Business-focused tone and language
                - Markdown formatting
                - Cute emojis for visual appeal
                - Professional yet engaging presentation

        Raises:
            AttributeError: If the `llm` object is not properly initialized or lacks invoke method.
            Exception: If the LLM service is unavailable or returns an error.
            TimeoutError: If the LLM request exceeds service timeout limits.

        Example:
            >>> sales_data = {"Q1": 150000, "Q2": 180000, "Q3": 165000, "Q4": 200000}
            >>> summary = summarize_data(sales_data)
            >>> print(summary)
            ## **Strong Growth Trajectory** 📈
            Revenue increased 33% year-over-year, with Q4 showing exceptional performance! 🚀✨

        Note:
            - Requires `llm` object to be available in the current scope
            - Response is truncated at first newline character due to stop parameter
            - Maximum token limit is set to 70 to enforce conciseness
            - Function assumes data can be meaningfully represented as string in prompt
            - Business analyst persona provides industry-agnostic strategic perspective
            - Markdown formatting enables rich text presentation in compatible displays

        Configuration:
            - Max tokens: 70 (enforces brevity)
            - Word limit: 30 (specified in prompt)
            - Stop sequence: ["\\n"] (ensures single-line response)
            - Output format: Markdown with emojis
            - Tone: Professional business analyst
        """
        prompt = load_prompt_from_file(summary_prompt_path)

        prompt = prompt.replace(r"{{data}}", data)

        response = llm.invoke(
            prompt=prompt,
            max_tokens=70,
            stop=["\n"],
        )

        return response.text.strip()

    tools = [restaurant_search, summarize_data]

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

    return graph
