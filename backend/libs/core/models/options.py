""" This module contains the OpenAIOptions class. """
from dataclasses import dataclass

@dataclass
class ChatConversationOptions:
    """Class used to manage the chat conversation
        and chain runnables together for the chat conversation"""
    system_prompt: str
    default_return_message: str

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

@dataclass
class VectorStoreOptions:
    """
    Options for configuring the vector store service.
    Args:
        endpoint: The vector store endpoint to use for retrieving documents.
        key: The vector store key to use when calling the service.
        semantic_configuration_name: The semantic configuration name
            used in the portal to describe the fields used for reranking.
    """
    endpoint: str
    key: str
    semantic_configuration_name: str
