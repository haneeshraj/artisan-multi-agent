import os
from google import genai
from google.genai import types
from openai import OpenAI
from anthropic import Anthropic
from datetime import datetime
from typing import Union, Dict
from dotenv import load_dotenv

load_dotenv()

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
    "gemini-2.0-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",

    # Anthropic models
    "claude-3-opus",
    "claude-3-haiku",
    "claude-3-sonnet",
    "claude-3.5-sonnet",
    "claude-3.5-haiku",
    "claude-3.7-sonnet",
    "claude-4-opus",
    

    # OpenAI models
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-3.5-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    
    
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

def query(model_name, prompt, temperature, max_tokens, cfg=None):
    """
    Query the specified LLM with the given prompt.
    
    Args:
        model_name (str): The name of the LLM to query.
        prompt (str): The prompt to send to the LLM.
        cfg (dict): Configuration dictionary containing API keys and other settings.
        
    Returns:
        str: The response from the LLM.
    """
    if not is_valid_llm(model_name):
        raise ValueError(f"Invalid model name: {model_name}. Available models: {get_available_llms()}")

    if model_name.startswith("gemini"):
        client = genai.Client(
            # api key from environment variable
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        
        contents = "\n".join(
        f"{entry['role'].capitalize()}: {entry['content']}" for entry in prompt
        )
        
        response = client.models.generate_content(
        model=model_name, 
        contents=contents,
        config= types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        )
        
        return response.text
        
    elif model_name.startswith("claude"):
        client = Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  
        )
        
        messages = [
            {"role": entry["role"], "content": entry["content"]}
            for entry in prompt
        ]
        
        
        completion = client.messages.create(
            model=model_name,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        
        return completion.content
        
    elif model_name.startswith("gpt"):
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        messages = [
            {"role": entry["role"], "content": entry["content"]}
            for entry in prompt
        ]
        
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        
        return completion.choices[0].message.content
        

