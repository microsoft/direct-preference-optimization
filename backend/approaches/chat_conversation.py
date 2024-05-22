"""Conversation logic for AI Chatbot."""
import dataclasses

from operator import itemgetter
from langchain_core.runnables import (RunnablePassthrough, RunnableLambda)
from models.chat_response import Answer, AnswerQueryConfig
from models.chat_response import ChatResponse, ChatResponseArgs
from approaches.multi_index_chat_builder import MultiIndexChatBuilder

@dataclasses.dataclass
class ChatConversationOptions:
    """Class used to manage the chat conversation
        and chain runnables together for the chat conversation"""
    system_prompt: str
    default_return_message: str

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

def _build_chain(builder: MultiIndexChatBuilder, chat_options: ChatConversationOptions):
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

def chat(
    builder: MultiIndexChatBuilder,
    chat_options: ChatConversationOptions,
    prompt: str) -> ChatResponse:
    """ Creating a chain of runnables that will fill the context variable
        in the template. Initially, this chain will get primary index
        documents and append the secondary index documents to the list.
        Then, it will sort and filter."""
    chain = _build_chain(builder, chat_options)
    answer = chain.invoke({"question": prompt})
    chat_answer = Answer(
        formatted_answer = answer.content,
        answer_query_config = AnswerQueryConfig(
            query=prompt,
            query_generation_prompt = None,
            query_result = None))
    chat_response_args = ChatResponseArgs(
        classification = None,
        data_points = None,
        error = None,
        suggested_classification = None
    )
    return ChatResponse(answer=chat_answer, chat_response_args=chat_response_args)
