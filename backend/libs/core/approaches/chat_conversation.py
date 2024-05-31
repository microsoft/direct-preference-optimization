"""Conversation logic for AI Chatbot."""
from operator import itemgetter
from langchain_core.runnables import (RunnablePassthrough, RunnableParallel, RunnableLambda)
from libs.core.approaches.multi_index_chat_builder import MultiIndexChatBuilder
from libs.core.models.options import ChatConversationOptions

def _default_route(options: ChatConversationOptions,
    builder: MultiIndexChatBuilder,
    context_info: dict):
    rated_documents = context_info["rated_response"]

    #if rated_documents and len(rated_documents) > 0 and rated_documents[0][2] > 3.5:
        #return builder.return_rated_message(rated_documents[0])
    
    return build_default_chain(builder=builder, chat_options=options)

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

def build_default_chain(
    builder: MultiIndexChatBuilder,
    chat_options: ChatConversationOptions):
    """Building the chain of runnables for the chat conversation."""

    docs = RunnableParallel(
        {
        "primary_documents": itemgetter("question") | RunnableLambda(builder.get_primary_documents),
        "secondary_documents": itemgetter("question") | RunnableLambda(builder.get_secondary_documents)
        })

    filtered_docs = docs | RunnableLambda(builder.sort_and_filter_documents)

    chain = {"context" : filtered_docs | builder.format_docs,
            "question": RunnablePassthrough() } | RunnableLambda(lambda info: _route(
        options = chat_options,
        builder = builder,
        context_info = info))

    return chain

def build_chain(
    builder: MultiIndexChatBuilder,
    chat_options: ChatConversationOptions):
    """Building the chain of runnables for the chat conversation."""
    full_chain = {
        "rated_response": itemgetter("question") 
        | RunnableLambda(builder.get_ratings),
            "question": lambda x: x["question"]
        } | RunnableLambda(lambda info: _default_route(options = chat_options, builder = builder, context_info = info))
    return full_chain
