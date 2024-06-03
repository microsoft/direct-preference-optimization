""" This module contains the OpenAIOptions class. """
from pydantic_settings import BaseSettings
from pydantic import Field

class ChatConversationOptions(BaseSettings):
    """Class used to manage the chat conversation
        and chain runnables together for the chat conversation"""
    system_prompt: str = Field()
    default_return_message: str = Field()

class ApiOptions(BaseSettings):
    """
    Options for configuring the OpenAI service.
    Args:
        endpoint: The OpenAI endpoint to use for chat conversation.
        api_key: The OpenAI api key to use when calling OpenAI.
        api_version: The OpenAI version of the endpoint.
    """
    endpoint: str = Field()
    api_key: str = Field()
    api_version: str = Field()

class ModelOptions(BaseSettings):
    """
    Options for configuring the OpenAI service.
    Args:
        deployment_model: The model used for the chat conversation.
        embedding_model: The embedding model used for creating vectors
         for searching and storing content.
        temperature: Value used to control the randomness of the output.
        n: Number of chat completions to generate for each prompt.
    """
    deployment_model: str = Field()
    embedding_model: str = Field()
    temperature: float = Field()
    max_tokens: int = Field()
    n: int = Field()

class OpenAIOptions(BaseSettings):
    """
    Options for configuring the OpenAI service.
    """
    api_options: ApiOptions = Field()
    ai_model_options: ModelOptions = Field()

class VectorStoreOptions(BaseSettings):
    """
    Options for configuring the vector store service.
    Args:
        endpoint: The vector store endpoint to use for retrieving documents.
        key: The vector store key to use when calling the service.
        semantic_configuration_name: The semantic configuration name
            used in the portal to describe the fields used for reranking.
    """
    endpoint: str = Field()
    key: str = Field()
    semantic_configuration_name: str = Field()

class StorageAccountOptions(BaseSettings):
    """
    Options for configuring the Storage Account where the original documents are stored.
    Args:
        url: The base url of the storage account.
    Note: The system expects that the container name will be returned with the document metadata.
    """
    account_name: str = Field()
    account_key: str = Field()
    use_account_key: bool = Field()
    @property
    def url(self):
        return f"https://{self.account_name}.blob.core.windows.net"

class MultiIndexVectorStoreOptions(BaseSettings):
    """Options for configuring the multi-index vector store service."""
    primary_index_name: str = Field()
    secondary_index_name: str = Field()
    vector_store_options: VectorStoreOptions = Field()
    open_ai_options: OpenAIOptions = Field()
    storage_account_options: StorageAccountOptions = Field()
