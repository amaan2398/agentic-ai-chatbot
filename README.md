# Agentic AI Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
