""" This module contains the OpenAIOptions class. """
from dataclasses import dataclass

@dataclass
class ApiOptions:
    """
    Options for configuring the OpenAI service.
    Args:
        endpoint: The OpenAI endpoint to use for chat conversation.
        api_key: The OpenAI api key to use when calling OpenAI.
        api_version: The OpenAI version of the endpoint.
    """
    endpoint: str
    api_key: str
    api_version: str

@dataclass
class ModelOptions:
    """
    Options for configuring the OpenAI service.
    Args:
        deployment_model: The model used for the chat conversation.
        embedding_model: The embedding model used for creating vectors
         for searching and storing content.
        temperature: Value used to control the randomness of the output.
        n: Number of chat completions to generate for each prompt.
    """
    deployment_model: str
    embedding_model: str
    temperature: float
    max_tokens: int
    n: int

@dataclass
class OpenAIOptions:
    """
    Options for configuring the OpenAI service.
    """
    api_options: ApiOptions
    model_options: ModelOptions
