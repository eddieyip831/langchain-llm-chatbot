# **LangChain LLM Chatbot**

A customizable chatbot application powered by LangChain and OpenAI, demonstrating advanced conversational memory and seamless integration with Streamlit for a web-based interface.

## **Features**

- **Interactive Chat Interface**: A user-friendly chat interface built with Streamlit.
- **Contextual Memory**: Retains conversation context across multiple turns, with adjustable memory size.
- **Dynamic Memory Adjustment**: Update memory size dynamically via a settings slider.
- **Session Management**: Supports session reset to clear history and start fresh.
- **Token Counting**: Utility to count tokens in input/output for API usage tracking.
- **Error Handling**: Graceful handling of errors, such as missing environment variables or API failures.
- **Customizable**: Easily extensible for different LLMs and configurations.

---

## **Getting Started**

### **Prerequisites**

- Python 3.10+
- OpenAI API Key
- LangChain and Streamlit libraries

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/langchain-llm-chatbot.git
   cd langchain-llm-chatbot
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your `.env` file:
   Create a `.env` file in the root directory with the following keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-3.5-turbo
   ```

---

## **Usage**

1. Run the Streamlit app:
   ```bash
   streamlit run src/chatbot/app/interface.py
   ```

2. Open the app in your browser:
   ```
   http://localhost:8501
   ```

3. Start chatting with the LangChain-powered chatbot!

---

## **Project Structure**

```plaintext
langchain-llm-chatbot/
├── src/
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── main.py         # ChatBot class and logic
│   │   ├── memory.py       # Memory management for conversation context
│   │   ├── utils.py        # Utility functions (e.g., token counting)
│   │   └── app/
│   │       └── interface.py  # Streamlit interface for the chatbot
│
├── tests/                  # Unit tests for all components
│   ├── test_chatbot.py
│   └── ...
│
├── requirements.txt        # Required Python packages
├── .env.example            # Template for environment variables
└── README.md               # Project documentation
```

---

## **Running Tests**

1. Install `pytest`:
   ```bash
   pip install pytest
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

3. View test results to ensure functionality is working as expected.

---

## **Key Features Tested**

| **Feature**                              | **Tested With**                          |
|------------------------------------------|------------------------------------------|
| Basic ChatBot Response                   | `test_chatbot_response`                  |
| Token Counting Utility                   | `test_count_tokens`                      |
| Contextual Memory                        | `test_chatbot_memory`                    |
| Memory Limit Enforcement                 | `test_chatbot_memory_limit`              |
| Session Reset                            | `test_session_reset`                     |
| Dynamic Memory Adjustment                | `test_slider_memory_adjustment`          |
| Handling Empty Input                     | `test_empty_input`                       |
| Handling Special Characters              | `test_special_characters`                |
| Handling Long User Inputs                | `test_long_input`                        |
| Edge Cases in Memory                     | `test_edge_cases_memory`                 |
| Error Handling                           | `test_error_handling`                    |

---

## **Contributing**

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your fork and submit a pull request.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

- [LangChain Documentation](https://python.langchain.com/docs/tutorials/chatbot/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API](https://openai.com/api/)

