""" Configuration file for the chat application """
from libs.core.models.options import (
    MultiIndexVectorStoreOptions,
    VectorStoreOptions,
    OpenAIOptions,
    ModelOptions,
    ApiOptions
)

from libs.core.approaches.chat_conversation import ChatConversationOptions

vector_store_options = VectorStoreOptions()
openai_options = OpenAIOptions(
    api_options = ApiOptions(),
    model_options = ModelOptions()
)
chat_options = ChatConversationOptions()
multi_index_options = MultiIndexVectorStoreOptions()
