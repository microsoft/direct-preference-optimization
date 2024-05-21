"""Main module for the FastAPI application."""

import os
import yaml

from fastapi import FastAPI
from dotenv import load_dotenv
from models.chat_request import Chat
from models.vector_store_options import VectorStoreOptions
from models.openai_options import OpenAIOptions
from approaches.multi_index_chat_builder import MultiIndexChatBuilder
from approaches.chat_conversation import ChatConversation

load_dotenv(override=True, dotenv_path=f"{os.getcwd()}/.env")

app = FastAPI()
@app.post("/chat")

def chat(chat_message: Chat):
    """API endpoint for chat conversation."""
    with open("chat_config.yaml", "r", encoding="utf-8") as file:
        chat_config = yaml.safe_load(file)
    chat_approach = chat_config["chat_approach"]
    default_return_message = chat_approach["default_return_message"]
    system_prompt = chat_config["chat_approach"]["system_prompt"]
    primary_index_name = chat_config["chat_approach"]["documents"]["primary_index_name"]
    secondary_index_name = chat_config["chat_approach"]["documents"]["secondary_index_name"]
    vector_store_options = VectorStoreOptions(
        os.environ["AZURE_SEARCH_ENDPOINT"],
        os.environ["AZURE_AI_SEARCH_API_KEY"],
        documents["semantic_configuration_name"],
    )

    openai_settings = chat_approach["openai_settings"]
    openai_options = OpenAIOptions(
        os.environ["AZURE_OPENAI_ENDPOINT"],
        os.environ["AZURE_OPENAI_API_KEY"],
        openai_settings["api_version" ],
        openai_settings["deployment"],
        openai_settings["embedding_model"],
        openai_settings["temperature"],
        openai_settings["max_tokens"],
        openai_settings["n"]
    )
    
    chat_builder = MultiIndexChatBuilder(
        primary_index_name,
        secondary_index_name,
        vector_store_options,
        openai_options
    )

    conversation = ChatConversation(
        system_prompt,
        default_return_message,
        chat_builder
    )

    response = conversation.chat(chat_message.dialog)

    return response.to_item()
