"""Conversation logic for AI Chatbot."""
from operator import itemgetter
from langchain_core.runnables import (RunnablePassthrough, RunnableLambda)
from libs.core.approaches.multi_index_chat_builder import MultiIndexChatBuilder
from libs.core.models.options import ChatConversationOptions

def _route(options: ChatConversationOptions,
    builder: MultiIndexChatBuilder,
    context_info: dict):
    """Route the conversation based on the context variable."""
    if not context_info["context"]:
        return builder.default_return_message(options.default_return_message)

    # Creating a chat template with a system message and a human message.
    # Both messages are passed as templates.
    model = builder.llm()
    chat_template = builder.chat_template(options.system_prompt)
    general_chain = chat_template | model
    return general_chain

def _get_context(
    primary_filter: RunnableLambda,
    secondary_filter: RunnableLambda,
    merge_filter: RunnableLambda):
    """Building the chain of runnables for the chat conversation."""
    return ({
        "context": {
            "primary_documents": itemgetter("question")
                | primary_filter,
            "secondary_documents": itemgetter("question") 
                | secondary_filter,
        } | merge_filter,
        "question": RunnablePassthrough(),
    })

def build_chain(
    builder: MultiIndexChatBuilder,
    chat_options: ChatConversationOptions):
    """Building the chain of runnables for the chat conversation."""
    return _get_context(
        RunnableLambda(builder.get_primary_documents),
        RunnableLambda(builder.get_secondary_documents),
        RunnableLambda(builder.sort_and_filter_documents)
        | builder.format_docs
    ) | RunnableLambda(lambda info: _route(
        options = chat_options,
        builder = builder,
        context_info = info))
