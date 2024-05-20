# import os
import yaml

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=f"{os.getcwd()}/.env")

from models.chat_request import Chat
from approaches.chat_conversation import ChatConversation

app = FastAPI()

@app.post("/chat")
def chat(chat_message: Chat):
    """API endpoint for chat conversation."""
    chat_config = yaml.safe_load(open("chat_config.yaml", "r"))
    conversation = ChatConversation(
        azure_openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_search_endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        azure_search_key=os.environ["AZURE_AI_SEARCH_API_KEY"]
    )

    response = conversation.chat(
        chat_config=chat_config,
        prompt=chat_message.dialog
    )

    return response.to_item()
