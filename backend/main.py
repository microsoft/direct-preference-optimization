import os
import yaml

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=f"{os.getcwd()}/.env")

from models.chat_request import Chat
from models.vector_store_options import VectorStoreOptions
from models.openai_options import OpenAIOptions
from approaches.chat_conversation import ChatConversation

app = FastAPI()


@app.post("/chat")
def chat(chat_message: Chat):
    """API endpoint for chat conversation."""
    chat_config = yaml.safe_load(open("chat_config.yaml", "r"))
    system_prompt = chat_config["chat_approach"]["system_prompt"]
    primary_index_name = chat_config["chat_approach"]["documents"]["primary_index_name"]
    secondary_index_name = chat_config["chat_approach"]["documents"]["secondary_index_name"]
    vector_store_options = VectorStoreOptions(
        os.environ["AZURE_SEARCH_ENDPOINT"],
        os.environ["AZURE_AI_SEARCH_API_KEY"],
        chat_config["chat_approach"]["documents"]["semantic_configuration_name"],
    )

    openai_options = OpenAIOptions(
        os.environ["AZURE_OPENAI_ENDPOINT"],
        os.environ["AZURE_OPENAI_API_KEY"],
         chat_config["chat_approach"]["openai_settings"]["api_version" ],
        chat_config["chat_approach"]["openai_settings"]["deployment"],
        chat_config["chat_approach"]["openai_settings"]["embedding_model"],
        chat_config["chat_approach"]["openai_settings"]["temperature"],
        chat_config["chat_approach"]["openai_settings"]["max_tokens"],
        chat_config["chat_approach"]["openai_settings"]["n"]
    )
    
    conversation = ChatConversation(
        primary_index_name,
        secondary_index_name,
        vector_store_options,
        openai_options
    )

    response = conversation.chat(system_prompt, chat_message.dialog)

    return response.to_item()