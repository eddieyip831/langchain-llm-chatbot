import os
import uuid
import logging
from datetime import datetime
import streamlit as st
from chatbot.main import ChatBot

"""
Streamlit interface for the LangChain LLM Chatbot.

This module provides a web-based interface for interacting with the LangChain-powered chatbot.
Users can input messages, view chat history, and adjust chatbot settings such as memory size.
"""

# Configure logging
log_filename = f"chatbot_debug_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Disable LangSmith logging (set environment variable)
os.environ["LANGCHAIN_TRACING"] = "false"

# Add custom CSS for sticky input and scrollable chat history
st.markdown(
    """
    <style>
    .chat-history {
        max-height: 300px; /* Restrict height of the chat history panel */
        overflow-y: auto; /* Add a vertical scroll bar if content overflows */
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .sticky-input {
        position: sticky;
        bottom: 0;
        background-color: #ffffff;
        padding: 10px;
        border-top: 1px solid #ddd;
    }
    .top-panel {
        padding: 10px;
        background-color: #f1f1f1;
        margin-bottom: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page title
st.title("LangChain LLM Chatbot")

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state["history"] = []  # Chat history

if "memory_size" not in st.session_state:
    st.session_state["memory_size"] = 5  # Memory size for conversation buffer

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())  # Generate a unique session ID

if "show_settings" not in st.session_state:
    st.session_state["show_settings"] = False  # Toggle for showing settings panel

# Sidebar toggle button for settings
with st.sidebar:
    if st.button("⚙️ Settings"):
        st.session_state["show_settings"] = not st.session_state["show_settings"]  # Toggle visibility

# Memory settings panel (only visible when toggled on)
if st.session_state["show_settings"]:
    st.sidebar.title("Memory Settings")
    st.sidebar.markdown("Adjust chatbot settings below:")

    # Memory size slider
    new_memory_size = st.sidebar.slider(
        "Memory Size (number of turns to retain)", min_value=1, max_value=10, value=st.session_state["memory_size"]
    )

    # Update memory size if changed
    if new_memory_size != st.session_state["memory_size"]:
        st.session_state["memory_size"] = new_memory_size

        # Reset the chatbot's memory with the new size
        st.session_state["chatbot"].reset_memory(new_size=new_memory_size)

        # Log the reset
        logger.debug(f"Memory reset with new buffer size: {new_memory_size}")

        # Notify the user
        st.sidebar.success(f"Memory reset to {new_memory_size} turns!")

# Initialize the chatbot with session memory size
if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = ChatBot(memory_size=st.session_state["memory_size"])

# Function to handle input submission
def handle_submit():
    user_input = st.session_state["user_input_temp"]
    if user_input:  # Only process if input is not empty
        # Get the chatbot response
        response = st.session_state["chatbot"].get_response(user_input)
        # Append to chat history
        st.session_state["history"].append({"user": user_input, "bot": response})
        st.session_state["user_input_temp"] = ""  # Clear input field after processing

# Top panel for instructions and new chat button
with st.container():
    st.markdown('<div class="top-panel">', unsafe_allow_html=True)
    st.write("Use the chatbot below to ask questions. Click 'New Chat' to start over.")
    if st.button("New Chat"):
        # Log the session reset
        logger.debug(f"Resetting chat session. Current session ID: {st.session_state['session_id']}")

        # Reset session state for chat history and chatbot
        st.session_state["history"] = []  # Clear chat history
        st.session_state["session_id"] = str(uuid.uuid4())  # Generate a new session ID
        st.session_state["chatbot"] = ChatBot(memory_size=st.session_state["memory_size"])  # Reset chatbot
        st.session_state["user_input_temp"] = ""  # Clear input field

        # Log the new session ID
        logger.debug(f"New session ID created: {st.session_state['session_id']}")
    st.markdown('</div>', unsafe_allow_html=True)

# Chat history panel
with st.container():
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    st.write("## Chat History:")
    for chat in st.session_state["history"]:
        st.write(f"**You**: {chat['user']}")
        st.write(f"**Bot**: {chat['bot']}")
    st.markdown('</div>', unsafe_allow_html=True)

# Sticky text input panel
with st.container():
    st.markdown('<div class="sticky-input">', unsafe_allow_html=True)

    # User input field with "Enter" support
    st.text_input(
        "Enter your message:",
        value="",
        key="user_input_temp",
        on_change=handle_submit,  # Trigger submission on "Enter"
    )

    st.markdown('</div>', unsafe_allow_html=True)  # Closing the div tag
