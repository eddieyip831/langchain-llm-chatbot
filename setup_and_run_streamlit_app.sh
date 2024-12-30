
#!/bin/bash

# Step 1: Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Step 4: Install dependencies
echo "Installing dependencies..."
pip install langchain openai python-dotenv tiktoken streamlit pytest

# Step 5: Test the Streamlit app
echo "Running Streamlit app..."
streamlit run src/chatbot/app/interface.py
