"""Main module for the FastAPI application."""
from fastapi import FastAPI

from models.rate_models import RateRequest
from models.chat_request import ChatRequest
from models.chat_response import (
    Answer,
    AnswerQueryConfig,
    ChatResponse,
    ChatResponseArgs,
    to_response_item
)

from libs.core.approaches.multi_index_chat_builder import MultiIndexChatBuilder
from libs.core.approaches.chat_conversation import build_chain
from libs.core.services.search_vector_index_service import (
    generate_embeddings,
    generate_azure_search_client,
    rate
)
from config import (
    multi_index_options,
    chat_options
)

chat_builder = MultiIndexChatBuilder(
    multi_index_options = multi_index_options
)
app = FastAPI()

@app.post("/rate")
def rate_response(rate_message: RateRequest):
    """API endpoint for rating the conversation."""
    embeddings = generate_embeddings(multi_index_options.openai_options)
    client = generate_azure_search_client(
        index_name="ratings",
        vector_store_options=multi_index_options.vector_store_options,
        embedding_function=embeddings,
    )
    response = rate(
        client = client,
        dialog_id = rate_message.dialog_id,
        rating = rate_message.rating,
        request = rate_message.request,
        response = rate_message.response
    )
    return response

@app.post("/chat")
def conversation(chat_message: ChatRequest):
    """API endpoint for chat conversation."""
    chain = build_chain(
        builder=chat_builder,
        chat_options=chat_options
    )

    answer = chain.invoke({"question": chat_message.dialog})
    chat_answer = Answer(
        formatted_answer = answer.content,
        answer_query_config = AnswerQueryConfig(
            query=chat_message.dialog,
            query_generation_prompt = None,
            query_result = None
        )
    )
    chat_response_args = ChatResponseArgs(
        classification = None,
        data_points = None,
        error = None,
        suggested_classification = None
    )
    response = ChatResponse(
        answer=chat_answer,
        chat_response_args=chat_response_args
    )

    return to_response_item(response)
