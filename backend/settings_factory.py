"""Monkey-patching factory methods for settings objects."""
import os

from dotenv import load_dotenv
import yaml
from libs.core.models.options import (
    ChatConversationOptions,
    MultiIndexVectorStoreOptions,
    OpenAIOptions,
    ApiOptions,
    ModelOptions,
    VectorStoreOptions,
    StorageAccountOptions
)

def _chat_conversation_from_settings(config: dict) -> ChatConversationOptions:
    return ChatConversationOptions(
        system_prompt=config["chat_approach"]["system_prompt"],
        default_return_message=config["chat_approach"]["default_return_message"]
    )
def _multi_index_vector_store_from_settings(config: dict) -> MultiIndexVectorStoreOptions:
    return MultiIndexVectorStoreOptions(
        primary_index_name=config["chat_approach"]["documents"]["primary_index_name"],
        secondary_index_name=config["chat_approach"]["documents"]["secondary_index_name"],
        vector_store_options=VectorStoreOptions.from_settings(config),
        open_ai_options=OpenAIOptions.from_settings(config),
        storage_account_options=StorageAccountOptions.from_settings(config)
    )
def _open_ai_options_from_settings(config: dict) -> OpenAIOptions:
    return OpenAIOptions(
        api_options=ApiOptions.from_settings(config),
        ai_model_options=ModelOptions.from_settings(config)
    )
def _api_options_from_settings(config: dict) -> ApiOptions:
    return ApiOptions(
        endpoint=config["AZURE_OPENAI_ENDPOINT"],
        api_key=config["AZURE_OPENAI_API_KEY"],
        api_version=config["chat_approach"]["openai_settings"]["api_version"]
    )
def _model_options_from_settings(config: dict) -> ModelOptions:
    return ModelOptions(
        deployment_model=config["chat_approach"]["openai_settings"]["deployment"],
        embedding_model=config["chat_approach"]["openai_settings"]["embedding_model"],
        temperature=config["chat_approach"]["openai_settings"]["temperature"],
        max_tokens=config["chat_approach"]["openai_settings"]["max_tokens"],
        n=config["chat_approach"]["openai_settings"]["n"]
    )
def _vector_store_options_from_settings(config: dict) -> VectorStoreOptions:
    docs = config["chat_approach"]["documents"]
    return VectorStoreOptions(
        endpoint=config["AZURE_SEARCH_ENDPOINT"],
        key=config["AZURE_AI_SEARCH_API_KEY"],
        semantic_configuration_name=docs["semantic_configuration_name"]
    )
def _storage_account_options_from_settings(config: dict) -> StorageAccountOptions:
    return StorageAccountOptions(
        account_name=config["STORAGE_ACCOUNT_NAME"]
    )

def load_config() -> dict:
    """Load the configuration file."""
    load_dotenv(override=True, dotenv_path=f"{os.getcwd()}/.env")
    with open("chat_config.yaml", "r", encoding="utf-8") as file:
        chat_config = yaml.safe_load(file)
    return chat_config | os.environ

ChatConversationOptions.from_settings = _chat_conversation_from_settings
MultiIndexVectorStoreOptions.from_settings = _multi_index_vector_store_from_settings
OpenAIOptions.from_settings = _open_ai_options_from_settings
ApiOptions.from_settings = _api_options_from_settings
ModelOptions.from_settings = _model_options_from_settings
VectorStoreOptions.from_settings = _vector_store_options_from_settings
StorageAccountOptions.from_settings = _storage_account_options_from_settings
