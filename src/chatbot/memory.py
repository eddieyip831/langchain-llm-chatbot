from langchain_core.messages import HumanMessage, AIMessage

class ConversationMemory:
    """
    A class to manage conversation history for a chatbot.

    Attributes:
        limit (int): Maximum number of conversation turns to retain in memory.
        buffer (list): A list of conversation messages, including user and AI inputs.
    """

    def __init__(self, limit=5):
        """
        Initializes the conversation memory with a specified size limit.

        Args:
            limit (int): Number of conversation turns to retain in memory.
        """
        self.limit = limit
        self.buffer = []

    def add_user_input(self, user_input):
        """
        Adds a user input message to the memory buffer.

        Args:
            user_input (str): The user's input message.
        """
        self.buffer.append(HumanMessage(content=user_input))
        if len(self.buffer) > self.limit:
            self.buffer.pop(0)

    def add_ai_response(self, ai_response):
        """
        Adds an AI response message to the memory buffer.

        Args:
            ai_response (str): The AI's response message.
        """
        self.buffer.append(AIMessage(content=ai_response))
        if len(self.buffer) > self.limit:
            self.buffer.pop(0)

    def get_buffered_messages(self):
        """
        Retrieves all messages currently stored in the memory buffer.

        Returns:
            list: A list of conversation messages (both user and AI messages).
        """
        return self.buffer


def get_memory(limit=5):
    """
    Factory function to create a ConversationMemory instance.

    Args:
        limit (int): Number of conversation turns to retain in memory.

    Returns:
        ConversationMemory: A memory object initialized with the specified limit.
    """
    return ConversationMemory(limit=limit)
