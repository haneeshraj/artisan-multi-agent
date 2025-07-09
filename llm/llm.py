import os

# Add yaml import
try:
    import yaml
except ImportError:
    print("Warning: PyYAML not found. Please install it with 'pip install pyyaml'")


AVAILABLE_LLMS = [
    # Gemini models
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-live",

    # Anthropic models
    "claude-3-opus",
    "claude-3-haiku",
    "claude-3.5-sonnet",

    # OpenAI models
    "gpt-4.1-nano",
    "gpt-3.5-turbo",
    "gpt-4.1-mini",
]



def is_valid_llm(model_name: str) -> bool:
    """
    Check if the provided model name is a valid LLM from the available list.
    
    Args:
        model_name (str): The name of the model to check.
        
    Returns:
        bool: True if the model is valid, False otherwise.
    """
    return model_name in AVAILABLE_LLMS

def get_available_llms() -> list:
    """
    Get a list of all available LLMs.
    
    Returns:
        list: A list of available LLM model names.
    """
    return AVAILABLE_LLMS.copy()  # Return a copy to prevent modification of the original list

