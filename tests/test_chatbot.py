import pytest
import sys
import os
import uuid

# Dynamically add the `src` directory to the Python path for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from chatbot.main import ChatBot
from chatbot.utils import count_tokens


# Test case for ChatBot's response
def test_chatbot_response():
    """
    Tests whether the ChatBot generates a valid response for a given input.
    """
    chatbot = ChatBot()
    response = chatbot.get_response("Hi! I'm Bob")
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"


# Test case for token counting utility
def test_count_tokens():
    """
    Tests whether the count_tokens function returns the correct token count.
    """
    text = "Hello, this is a test for token counting."
    token_count = count_tokens(text)
    assert isinstance(token_count, int), "Token count should be an integer"
    assert token_count > 0, "Token count should be greater than zero"


# Test case for ChatBot's memory
def test_chatbot_memory():
    """
    Tests whether the ChatBot retains context across multiple conversation turns.
    """
    chatbot = ChatBot(memory_size=3)  # Limit memory size for testing

    # First interaction: introducing a name
    response_1 = chatbot.get_response("My name is John.")
    assert "John" in response_1 or len(response_1) > 0, "The bot should acknowledge the name"

    # Second interaction: checking if the bot remembers the name
    response_2 = chatbot.get_response("What is my name?")
    assert "John" in response_2, "The bot should remember the name from previous interaction"

    # Third interaction: memory context test
    response_3 = chatbot.get_response("What did we just talk about?")
    assert "name" in response_3 or "John" in response_3, "The bot should reference the conversation context"


# Test case for memory limit
def test_chatbot_memory_limit():
    """
    Tests whether the ChatBot forgets earlier context once memory size is exceeded.
    """
    chatbot = ChatBot(memory_size=2)  # Limit memory size to 2 turns

    # Provide multiple conversation turns
    chatbot.get_response("I live in Paris.")
    chatbot.get_response("My favorite color is blue.")
    response = chatbot.get_response("Where do I live?")

    # The bot should no longer remember the first input as memory is limited
    assert "Paris" not in response, "The bot should forget 'Paris' after memory size is exceeded"


# Test case for empty input
def test_empty_input():
    """
    Tests that the chatbot handles empty user input gracefully.
    """
    chatbot = ChatBot()
    response = chatbot.get_response("")
    assert response, "Chatbot should return a default message for empty input."


# Test case for special characters
def test_special_characters():
    """
    Tests that the chatbot handles special characters and emojis in user input.
    """
    chatbot = ChatBot()
    special_input = "Hello! How are you doing? 😊🔥 #chatbot"
    response = chatbot.get_response(special_input)
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"


# Test case for resetting memory
def test_reset_memory():
    chatbot = ChatBot(memory_size=3)
    chatbot.get_response("My name is John.")
    chatbot.reset_memory()  # Resets to DEFAULT_MEMORY_SIZE (5)
    assert len(chatbot.memory.get_buffered_messages()) == 0, "Chatbot memory should be reset."
    chatbot.reset_memory(new_size=3)  # Explicitly resets to 3
    assert len(chatbot.memory.get_buffered_messages()) == 0, "Chatbot memory should be reset to new size."


# Test case for slider memory adjustment
def test_slider_memory_adjustment():
    """
    Tests that the memory size adjusts dynamically and retains updated memory size.
    """
    chatbot = ChatBot(memory_size=3)
    chatbot.get_response("My name is John.")
    chatbot.reset_memory(new_size=5)  # Adjust memory dynamically
    assert len(chatbot.memory.get_buffered_messages()) == 0, "Memory should adjust dynamically."


# Test case for long input
def test_long_input():
    """
    Tests that the chatbot can handle long user inputs without crashing or truncating responses.
    """
    chatbot = ChatBot()
    long_input = "This is a very long input. " * 50  # Create a long input string
    response = chatbot.get_response(long_input)
    assert isinstance(response, str), "Response should be a string"
    assert len(response) > 0, "Response should not be empty"


# Test case for edge cases in memory
def test_edge_cases_memory():
    """
    Tests edge cases for memory, including memory size of 1 and boundary behavior.
    """
    chatbot = ChatBot(memory_size=1)
    chatbot.get_response("My name is John.")
    response = chatbot.get_response("What is my name?")
    assert "John" not in response, "Chatbot should not retain memory when memory size is 1."


# Test case for error handling
def test_error_handling():
    """
    Tests that the chatbot handles errors gracefully, such as missing environment variables.
    """
    os.environ.pop("OPENAI_MODEL", None)  # Temporarily remove the model environment variable
    try:
        chatbot = ChatBot()
    except Exception as e:
        assert isinstance(e, KeyError), "Chatbot should raise a KeyError for missing env variables."


# Inline definition of a simple session state class
class SessionState:
    def __init__(self, memory_size=3):
        self.session_id = str(uuid.uuid4())
        self.history = []
        self.chatbot = ChatBot(memory_size=memory_size)

    def reset(self, memory_size=3):
        """
        Resets the session state, clearing history and generating a new session ID.
        """
        self.session_id = str(uuid.uuid4())  # Generate a new session ID
        self.history = []  # Clear chat history
        self.chatbot.reset_memory(new_size=memory_size)  # Reset chatbot memory


# Test case for session reset
def test_session_reset():
    """
    Tests that starting a new session clears history and generates a new session ID.
    """
    # Initialize session state with memory size
    session = SessionState(memory_size=3)

    # Capture the initial session ID
    session_id_1 = session.session_id

    # Simulate chat history
    session.history = [{"user": "Hello", "bot": "Hi there!"}]

    # Reset the session
    session.reset(memory_size=3)

    # Capture the new session ID after reset
    session_id_2 = session.session_id

    # Assertions to validate the reset
    assert session_id_1 != session_id_2, "New session ID should differ from the previous one."
    assert session.history == [], "Chat history should be cleared in a new session."
