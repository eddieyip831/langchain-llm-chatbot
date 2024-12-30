from setuptools import setup, find_packages

setup(
    name="langchain-llm-chatbot",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "langchain-community", 
        "openai", 
        "python-dotenv", 
        "tiktoken", 
        "streamlit", 
        "pytest"
    ],
)
