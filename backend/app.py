import os
import yaml

from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=f"{os.getcwd()}/backend/.env")

from approaches.chatconversation import ChatConversation

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    chat_config = yaml.safe_load(open("backend/chat_config.yaml", "r"))
    message = request.json.get("dialog")
    conversation = ChatConversation(
        azure_openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_search_endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        azure_search_key=os.environ["AZURE_AI_SEARCH_API_KEY"]
    )
    
    response = conversation.chat(
        chat_config=chat_config,
        prompt=message
    )

    return jsonify(response.to_item())

if __name__ == '__main__':
    app.run(debug=True)