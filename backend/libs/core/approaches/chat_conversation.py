"""Conversation logic for AI Chatbot."""
from operator import itemgetter
from langchain_core.runnables import (RunnablePassthrough, RunnableParallel, RunnableLambda)
from langchain_core.output_parsers import JsonOutputParser
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

def build_chain(
    builder: MultiIndexChatBuilder,
    chat_options: ChatConversationOptions):
    """Building the chain of runnables for the chat conversation."""

    docs = RunnableParallel(
        {
        "primary_documents": itemgetter("question") | RunnableLambda(builder.get_primary_documents),
        "secondary_documents": itemgetter("question") | RunnableLambda(builder.get_secondary_documents)
        })

    filtered_docs = docs | RunnableLambda(builder.sort_and_filter_documents)

    parser = JsonOutputParser()

    chain = {"context" : filtered_docs | builder.format_docs,
            "question": RunnablePassthrough() } | RunnableLambda(lambda info: _route(
        options = chat_options,
        builder = builder,
        context_info = info)) | parser

    return chain
