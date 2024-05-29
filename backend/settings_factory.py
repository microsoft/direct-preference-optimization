"""Monkey-patching factory methods for settings objects."""
import os
from libs.core.models.options import (
    ChatConversationOptions,
    MultiIndexVectorStoreOptions,
    OpenAIOptions,
    ApiOptions,
    ModelOptions,
    VectorStoreOptions
)

def _chat_conversation_from_settings(config: dict) -> ChatConversationOptions:
    return ChatConversationOptions(
        system_prompt=config.get('system_prompt'),
        default_return_message=config.get('default_return_message')
    )
def _multi_index_vector_store_from_settings(config: dict) -> MultiIndexVectorStoreOptions:
    return MultiIndexVectorStoreOptions(
        primary_index_name=config.get('primary_index_name'),
        secondary_index_name=config.get('secondary_index_name'),
        vector_store_options=VectorStoreOptions.from_settings(config),
        open_ai_options=OpenAIOptions.from_settings(config)
    )
def _open_ai_options_from_settings(config: dict) -> OpenAIOptions:
    return OpenAIOptions(
        api_options=ApiOptions.from_settings(config),
        model_options=ModelOptions.from_settings(config)
    )
def _api_options_from_settings(config: dict) -> ApiOptions:
    return ApiOptions(
        endpoint=config.get('endpoint'),
        api_key=config.get('api_key'),
        api_version=config.get('api_version')
    )
def _model_options_from_settings(config: dict) -> ModelOptions:
    return ModelOptions(
        deployment_model=config.get('deployment_model'),
        embedding_model=config.get('embedding_model'),
        temperature=config.get('temperature'),
        max_tokens=config.get('max_tokens'),
        n=config.get('n')
    )
def _vector_store_options_from_settings(config: dict) -> VectorStoreOptions:
    return VectorStoreOptions(
        endpoint=config.get('endpoint'),
        key=config.get('key'),
        semantic_configuration_name=config.get('semantic_configuration_name')
    )

def load_config() -> dict:
    return os.environ

ChatConversationOptions.from_settings = _chat_conversation_from_settings
MultiIndexVectorStoreOptions.from_settings = _multi_index_vector_store_from_settings
OpenAIOptions.from_settings = _open_ai_options_from_settings
ApiOptions.from_settings = _api_options_from_settings
ModelOptions.from_settings = _model_options_from_settings
VectorStoreOptions.from_settings = _vector_store_options_from_settings
