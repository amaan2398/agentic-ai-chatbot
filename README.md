# Agentic AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Built with LangChain](https://img.shields.io/badge/Built%20with-LangChain-purple)](https://www.langchain.com/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Built with LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-1de9b6)](https://langchain-ai.github.io/langgraph/)


An intelligent, agentic AI chatbot capable of understanding complex queries and performing actions by integrating with various third-party APIs. This chatbot can fetch movie information, find local businesses, and more. 🤖



---

## ✨ Features

* **Natural Language Understanding (NLU):** Powered by a sophisticated language model to understand user intent.
* **Agentic Behavior:** Can autonomously decide which tool or API to use based on the user's query.
* **Multi-API Integration:** Seamlessly connects to external services like TMDB and Yelp to provide rich, real-time information.
* **Conversational Memory:** Remembers the context of the conversation for a more natural interaction.
* **Extensible Architecture:** Easily add new tools and API integrations.

---

## 🛠️ API Integrations

This chatbot leverages powerful external APIs to provide a wide range of functionalities.

### The Movie Database (TMDB) API 🎬

To handle all movie and TV show-related queries, the chatbot integrates with the **TMDB API**. This allows the agent to access a massive, community-built database of film and television content.

* **Functionality:**
    * Fetch detailed information about specific movies (e.g., "Tell me about the movie Inception").
    * Get a list of popular, top-rated, or currently playing movies.
    * Find movies based on genre, actor, or director.
    * Provide personalized movie recommendations.
* **Usage Example:** A user asking, "What other movies has Christopher Nolan directed?" will trigger the TMDB tool to fetch the relevant filmography.



### Yelp Fusion API  Yelp

For location-based and local business queries, the chatbot uses the **Yelp Fusion API**. This enables the agent to act as a local guide, helping users discover businesses, restaurants, and services around them.

* **Functionality:**
    * Search for local businesses by category (e.g., "Find coffee shops near me").
    * Get details about a specific business, including its rating, address, phone number, and reviews.
    * Find the best local spots based on user preferences (e.g., "top-rated Italian restaurants in downtown").
* **Usage Example:** A user query like, "I'm looking for a good place for dinner in Hyderabad" prompts the agent to use the Yelp tool to search for highly-rated restaurants in that city.

---

## 🧠 How It Works: The Agentic Flow

Below is a visualization of the core agentic graph:

![Chatbot Graph Visualization](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/chatbot_lang_graph.png)


---

## 📸 Chatbot in Action: Conversational Flows

Here’s a look at how the chatbot handles real-world scenarios, from a simple greeting to complex, multi-step queries.

### 1. Simple Greeting

The conversation starts with a simple, natural interaction.

![Chatbot greeting the user](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/screenshots/Hello%20Screen.png)

### 2. Movie Suggestions (Multi-Step Query)

This example showcases how the agent gathers information to provide personalized movie recommendations using **The Movie Database (TMDB)**.

#### Step 1: Initial Request

The user asks for a recommendation without providing any context.

![Chatbot asked for more clarity](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/screenshots/Movie%20suggestion%20s-1.png)

#### Step 2: Gathering Context & Delivering Results

The user provides a movie they like. The agent uses this context to query the TMDB API and fetches detailed information, summarizing the results in a list.

![Chatbot uses provided details and fetch data from TMDB and summarize and show in card formate](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/screenshots/Movie%20suggestion%20s-2.png)

### 3. Restaurant Recommendations (Complex Conversational Flow)

This flow demonstrates the agent's ability to handle ambiguity by asking clarifying questions until it has enough information to use the **Yelp API**.

#### Step 1: Vague Initial Request

The user asks for restaurants but provides no specific details. The AI asks for the necessary information.

![Chatbot asked for more clarity](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/screenshots/Restaurant%20suggestion%20s-1.png)

#### Step 2: Partial Information Provided

The user provides some, but not all, of the required details. The AI recognizes what's missing and asks for it specifically.

![Chatbot recognizes what's missing and asks for it specifically.](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/screenshots/Restaurant%20suggestion%20s-2.png)

#### Step 3: All Information Gathered & Action Executed

The user provides the final piece of information. The agent now has everything it needs. It queries the Yelp API, retrieves a list of matching restaurants, and presents them with a helpful summary.

![Chatbot searching for restaurants using Yelp](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/static/screenshots/Restaurant%20suggestion%20s-3.png)



---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* Python 3.8+
* Pip package manager
* API keys for TMDB and Yelp

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/amaan2398/agentic-ai-chatbot.git
    cd agentic-ai-chatbot
    ```

2.  **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```
    TMDB_API_KEY="your_tmdb_api_key_here"
    YELP_API_KEY="your_yelp_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key"
    ```

### Usage

Run the main application file to start the chatbot:
```sh
python main.py
````

You can now interact with the chatbot from your terminal.

-----

## 💻 Technologies Used

  * **Backend:** Python
  * **LLM:** OpenAI GPT series (or any other compatible model)
  * **Frameworks:** LangChain, FastAPI (optional for API deployment)
  * **APIs:**
      * The Movie Database (TMDB) API
      * Yelp Fusion API

-----

## Project Report

For a detailed analysis of this project, including our methodology, findings, and final conclusions, please see the full project report. The document provides an in-depth look at the entire project lifecycle.

📄 **[View the Full Project Report](https://github.com/amaan2398/agentic-ai-chatbot/blob/main/documents/Chatbot%20Project%20Report.pdf)**

-----

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improving the chatbot, please feel free to create a pull request or open an issue.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

-----

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
