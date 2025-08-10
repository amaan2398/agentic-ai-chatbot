import json

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from utils.generic import *

# Initialize Streamlit app configuration
st.set_page_config(
    page_title="Restaurant and Movie Recommendation ChatBot", page_icon="🤖", layout="wide"
)

# Header
st.title("Restaurant and Movie Recommendation ChatBot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Iterate through the messages in session_state and display them.
for message in st.session_state.messages:
    # Use st.chat_message to display messages, distinguishing between 'user' and 'assistant'.
    with st.chat_message(message["role"]):
        if message.get("type", "generic") == "generic":
            st.markdown(message["content"])

def render_movie_card(movie):
    """Returns the HTML string for a single movie card with poster image."""

    title = movie["title"]
    rating = movie["rating"]
    language = movie["language"]
    poster_img = movie["poster-img"]

    return f"""
        <div style="
            border: 1px solid var(--border-color);
            background-color: var(--secondary-background-color);
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            min-width: 250px;
            max-width: 300px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: var(--text-color);
        ">
            <h4>🎬 {title}</h4>
            <div style="
                border-radius: 8px;
                overflow: hidden;
                margin-bottom: 10px;
                text-align: center;
            ">
                <img src="{poster_img}" alt="{title} Poster" style="width: 100%; height: auto; display: block;">
            </div>
            <p style="margin: 4px 0;"><strong>⭐ Rating:</strong> {rating:.1f}</p>
            <p style="margin: 4px 0;"><strong>🌎 Language:</strong> {language.upper()}</p>
        </div>
    """

def render_restaurant_card(restaurant):
    """Returns the HTML string for a single restaurant card, now with an interactive map using an iframe."""
    print("Restaurant data:", restaurant)
    # Build address from location components
    location = restaurant["location"]
    address = f"{location['address1']}, {location['city']}, {location['state']} {location['zip_code']}"

    # The URL for Google Maps embeds
    iframe_url = f"https://maps.google.com/maps?q={address}&output=embed"
    maps_link = f"http://maps.google.com/?q={address}"

    return f"""
        <div style="
            border: 1px solid var(--border-color);
            background-color: var(--secondary-background-color);
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            min-width: 300px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <h4><a href="{maps_link}" target="_blank" style="text-decoration: none; color: var(--text-color);">{restaurant["name"]}</a></h4>
            <div style="
                border-radius: 8px;
                overflow: hidden;
                margin-top: 10px;
                margin-bottom: 10px;
            ">
                <iframe
                    src="{iframe_url}"
                    style="border:0;"
                    width="100%"
                    height="150"
                    allowfullscreen=""
                    loading="lazy"
                    referrerpolicy="no-referrer">
                </iframe>
            </div>
            <p style="margin-top: 0; color: var(--text-color);"><strong>⭐ Rating:</strong> {restaurant.get("rating", "N/A")}</p>
            <p style="color: var(--text-color);"><strong>📍 Address:</strong> {address}</p>
            <p style="color: var(--text-color);"><strong>💰 Price:</strong> {restaurant.get("price", "N/A")}</p>
            <p style="color: var(--text-color);"><strong>📞 Phone:</strong> {restaurant.get("display_phone", "N/A")}</p>
            <p style="color: var(--text-color);"><strong>🍽️ Cuisine:</strong> {", ".join([cat["title"] for cat in restaurant.get("categories", [])])}</p>
        </div>
    """


def get_llm():
    """Get or create LLM using session state"""
    if "llm" not in st.session_state:
        with st.spinner("Initializing AI model..."):
            st.session_state.llm = init_and_load_env()
    return st.session_state.llm


# In your main app code
llm = get_llm()

if "chat_state" not in st.session_state:
    base_prompt = load_prompt_from_file(r"static/prompts/base.txt")
    st.session_state.chat_state = {"messages": [SystemMessage(content=base_prompt)]}

if prompt := st.chat_input("What's on your mind?"):
    # st.session_state.messages.append({"role": "user", "content": prompt})
    print("st.session_state.chat_state:", st.session_state.chat_state)
    st.session_state.chat_state["messages"].append(HumanMessage(content=prompt))
    # Display the user message immediately
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        for chunk in llm.stream(st.session_state.chat_state):
            # Generate response using the LLM
            print("chunk:", chunk)
            if chunk.get("chatbot"):
                last_msg = chunk["chatbot"]["messages"][-1]
                st.session_state.chat_state["messages"].append(last_msg)

                # Display latest AI message
                if isinstance(last_msg, AIMessage):
                    response_container.write(last_msg.content)
            elif chunk.get("tools"):
                last_msg = chunk["tools"]["messages"][-1]
                tool_name = last_msg.name
                st.session_state.chat_state["messages"] = st.session_state.chat_state[
                    "messages"
                ][:1]
                
                # Display latest AI message
                if tool_name == "get_movie_recommendations":
                    st.markdown("### 🎞️ Recommended Movies")
                    # Container for the horizontally scrolling cards
                    movies = json.loads(last_msg.content)['recommendations']
                    card_html = "".join(
                        [render_movie_card(r) for r in movies]
                    )
                    st.markdown(
                        f"""
                        <div style="
                            display: flex;
                            flex-direction: row;
                            overflow-x: auto;
                            padding: 10px 0;
                            -webkit-overflow-scrolling: touch; /* For smoother scrolling on iOS */
                            scrollbar-width: thin; /* For Firefox */
                            scrollbar-color: #A9A9A9 #F1F0F0; /* For Firefox */
                        ">
                            {card_html}
                        

                        """,
                        unsafe_allow_html=True,
                    )
                if tool_name == "restaurant_search":
                    st.markdown("### 🍴 Recommended Restaurants")
                    # Container for the horizontally scrolling cards
                    restaurants = json.loads(last_msg.content)
                    card_html = "".join(
                        [render_restaurant_card(r) for r in restaurants]
                    )
                    st.markdown(
                        f"""
                        <div style="
                            display: flex;
                            flex-direction: row;
                            overflow-x: auto;
                            padding: 10px 0;
                            -webkit-overflow-scrolling: touch; /* For smoother scrolling on iOS */
                            scrollbar-width: thin; /* For Firefox */
                            scrollbar-color: #A9A9A9 #F1F0F0; /* For Firefox */
                        ">
                            {card_html}

                        """,
                        unsafe_allow_html=True,
                    )
