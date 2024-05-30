""" Configuration file for the chat application """
from libs.core.models.options import (
    MultiIndexVectorStoreOptions,
    VectorStoreOptions,
    OpenAIOptions,
)
from settings_factory import load_config

from libs.core.approaches.chat_conversation import ChatConversationOptions

config = load_config()
vector_store_options = VectorStoreOptions.from_settings(config)
openai_options = OpenAIOptions.from_settings(config)
chat_options = ChatConversationOptions.from_settings(config)
multi_index_options = MultiIndexVectorStoreOptions.from_settings(config)
