import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .memory import get_memory

# Default memory size constant
DEFAULT_MEMORY_SIZE = 5

class ChatBot:
    """
    A chatbot class that uses LangChain and OpenAI models to generate responses 
    while maintaining conversational context with memory.

    Attributes:
        model (ChatOpenAI): The OpenAI model used for generating responses.
        memory (ConversationMemory): A memory object to retain conversation history.
    """

    def __init__(self, memory_size=DEFAULT_MEMORY_SIZE):
        """
        Initializes the chatbot with a specified memory size.

        Args:
            memory_size (int): Number of conversation turns to retain in memory.
        """
        self.model = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"), temperature=0.7
        )
        self._memory_size = memory_size  # Private attribute
        self.memory = get_memory(self._memory_size)

    @property
    def memory_size(self):
        """
        Gets the current memory size.

        Returns:
            int: The current memory buffer size.
        """
        return self._memory_size

    @memory_size.setter
    def memory_size(self, new_size):
        """
        Sets a new memory size and reinitializes the memory.

        Args:
            new_size (int): The new memory buffer size.
        """
        if new_size <= 0:
            raise ValueError("Memory size must be a positive integer.")
        self._memory_size = new_size
        self.memory = get_memory(self._memory_size)  # Reinitialize memory with new size

    def get_response(self, user_input):
        """
        Generates a response from the chatbot based on user input, 
        while incorporating the retained memory context.

        Args:
            user_input (str): The user's input message.

        Returns:
            str: The chatbot's response to the input message.
        """
        # Add user input to memory
        self.memory.add_user_input(user_input)

        # Construct the conversation messages from memory
        messages = [SystemMessage(content="You are a helpful AI assistant.")]
        messages += self.memory.get_buffered_messages()

        # Get the AI model's response
        response = self.model.invoke(messages)

        # Add AI response to memory
        self.memory.add_ai_response(response.content)

        return response.content

    def reset_memory(self, new_size=None):
        """
        Resets the chatbot's memory with a new buffer size if provided.

        Args:
            new_size (int, optional): The new memory buffer size. If None, uses the default size.
        """
        self.memory_size = new_size if new_size is not None else DEFAULT_MEMORY_SIZE
