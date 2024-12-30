import tiktoken

def count_tokens(text, model_name="gpt-3.5-turbo"):
    """
    Counts tokens in the given text using the tiktoken library.
    
    Args:
        text (str): The text to count tokens for.
        model_name (str): The model for which to count tokens.

    Returns:
        int: The number of tokens in the text.
    """
    enc = tiktoken.encoding_for_model(model_name)
    return len(enc.encode(text))
