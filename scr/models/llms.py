from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import json
import os

"""Load Large Language Model.

    Args:
        model_name (str): The name of the model to load.

    Raises:
        ValueError: If the model_name is not recognized.

    Returns:
        ChatOpenAI: An instance of ChatOpenAI configured for the specified model.
    """


from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def load_llm(api_key, model_name):
    if model_name == "gpt-4o-mini":
        return ChatOpenAI(
            api_key=api_key,
            model=model_name,
            temperature=0.0,
            max_tokens=1000,
        )
    elif model_name == "gemini-pro" or model_name == "gemini-1.5-pro-002":
        return ChatGoogleGenerativeAI(
            api_key=api_key,
            model=model_name,
            temperature=1.0,
            max_tokens=1000,
        )
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")



# Example usage
# api_key = "your API"
# llm = load_llm("gemini 1.5")
# response = llm("Hello, how can I help you?")
# print(response)
