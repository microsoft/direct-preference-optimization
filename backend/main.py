"""Main module for the FastAPI application."""

import os
import yaml

from fastapi import FastAPI
from dotenv import load_dotenv
from models.rate_models import RateRequest
from models.chat_request import ChatRequest
from models.chat_response import (
    Answer,
    AnswerQueryConfig,
    ChatResponse,
    ChatResponseArgs,
    to_response_item
)
from libs.core.models.vector_store_options import VectorStoreOptions
from libs.core.models.openai_options import OpenAIOptions, ModelOptions, ApiOptions
from libs.core.approaches.multi_index_chat_builder import MultiIndexChatBuilder
from libs.core.approaches.chat_conversation import ChatConversationOptions, build_chain
from libs.core.services.search_vector_index_service import (
    generate_embeddings,
    generate_azure_search_client,
    rate
)

load_dotenv(override=True, dotenv_path=f"{os.getcwd()}/.env")
with open("chat_config.yaml", "r", encoding="utf-8") as file:
    chat_config = yaml.safe_load(file)
chat_approach = chat_config["chat_approach"]
default_return_message = chat_approach["default_return_message"]
system_prompt = chat_approach["system_prompt"]
documents = chat_approach["documents"]
primary_index_name = documents["primary_index_name"]
secondary_index_name = documents["secondary_index_name"]
environ = os.environ
vector_store_options = VectorStoreOptions(
    environ["AZURE_SEARCH_ENDPOINT"],
    environ["AZURE_AI_SEARCH_API_KEY"],
    documents["semantic_configuration_name"],
)

openai_settings = chat_approach["openai_settings"]
openai_options = OpenAIOptions(
    api_options = ApiOptions(
        endpoint = environ["AZURE_OPENAI_ENDPOINT"],
        api_key = environ["AZURE_OPENAI_API_KEY"],
        api_version = openai_settings["api_version"]),
    model_options = ModelOptions(
        deployment_model = openai_settings["deployment"],
        embedding_model = openai_settings["embedding_model"],
        temperature = openai_settings["temperature"],
        max_tokens = openai_settings["max_tokens"],
        n = openai_settings["n"]
    )
)

chat_options = ChatConversationOptions(
    system_prompt,
    default_return_message
)

chat_builder = MultiIndexChatBuilder(
    primary_index_name,
    secondary_index_name,
    vector_store_options,
    openai_options
)

app = FastAPI()

@app.post("/rate")
def rate_response(rate_message: RateRequest):
    """API endpoint for rating the conversation."""
    embeddings = generate_embeddings(openai_options)
    client = generate_azure_search_client(
        index_name="ratings",
        vector_store_options=vector_store_options,
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

    response = chain.invoke({"question": chat_message.dialog})
    chat_answer = Answer(
        formatted_answer = response["answer"].content,
        citations = response["filtered_docs"],
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
