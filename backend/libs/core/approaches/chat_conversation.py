"""Conversation logic for AI Chatbot."""
from operator import itemgetter
from langchain_core.runnables import (RunnablePassthrough, RunnableParallel, RunnableLambda)
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from libs.core.approaches.multi_index_chat_builder import MultiIndexChatBuilder
from libs.core.models.options import ChatConversationOptions
from libs.core.models.cited_answer import CitedAnswer

def _route(options: ChatConversationOptions,
    builder: MultiIndexChatBuilder,
    context_info: dict):
    """Route the conversation based on the context variable."""
    if not context_info["context"]:
        return builder.default_return_message(options.default_return_message)

    # Creating a chat template with a system message and a human message.
    # Both messages are passed as templates.
    
    output_parser = JsonOutputKeyToolsParser(key_name="CitedAnswer", first_tool_only=True)
    model = builder.llm()

    llm_with_tool = model.bind_tools(
        [CitedAnswer],
        tool_choice="CitedAnswer",
    )

    chat_template = builder.chat_template(options.system_prompt)
    general_chain = chat_template | llm_with_tool | output_parser
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

    chain = {"context" : filtered_docs | builder.format_docs,
            "question": RunnablePassthrough() } | RunnableLambda(lambda info: _route(
        options = chat_options,
        builder = builder,
        context_info = info))

    return chain
