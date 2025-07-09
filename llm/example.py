#!/usr/bin/env python3
"""
Example usage of the LLM module.
"""

from llm import (
    get_content_gen_model,
    get_eval_model,
    get_code_gen_model,
    get_available_llms,
    is_valid_llm
)

def main():
    # Get all available LLMs
    print("Available LLMs:")
    for model in get_available_llms():
        print(f"  - {model}")
    
    # Get models from config
    print("\nModels from config.yaml:")
    print(f"  Content Generation: {get_content_gen_model()}")
    print(f"  Evaluation: {get_eval_model()}")
    print(f"  Code Generation: {get_code_gen_model()}")
    
    # Overriding with specific models
    print("\nOverriding with specific models:")
    print(f"  Content Generation: {get_content_gen_model('claude-3-opus')}")
    print(f"  Evaluation: {get_eval_model('gemini-2.5-pro')}")
    
    # Using an invalid model (will use default)
    print("\nUsing an invalid model (will use default):")
    print(f"  Code Generation: {get_code_gen_model('non-existent-model')}")
    
    # Check if a model is valid
    test_model = "gpt-4"
    print(f"\nIs '{test_model}' valid? {is_valid_llm(test_model)}")
    print(f"Is 'claude-3-opus' valid? {is_valid_llm('claude-3-opus')}")

if __name__ == "__main__":
    main()
