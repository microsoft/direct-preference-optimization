from textwrap import dedent

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import ( HumanMessage, SystemMessage)
from models.chat_response import ChatResponse
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from models.chat_response import Answer

class ChatConversation():

    def __init__(
            self, 
            azure_openai_endpoint: str,
            azure_openai_api_key: str,
            azure_search_endpoint: str = None,
            azure_search_key: str = None,
    ):
        self.__azure_openai_endpoint = azure_openai_endpoint
        self.__azure_openai_api_key = azure_openai_api_key
        self.__azure_search_endpoint = azure_search_endpoint
        self.__azure_search_key = azure_search_key

    def chat(self, chat_config, prompt: str) -> ChatResponse:
        openai_api_version = chat_config["chat_approach"]["openai_settings"]["api_version"]
        openai_deployment = chat_config["chat_approach"]["openai_settings"]["deployment"]
        openai_temperature = chat_config["chat_approach"]["openai_settings"]["temperature"]
        openai_max_tokens = chat_config["chat_approach"]["openai_settings"]["max_tokens"]
        openai_n = chat_config["chat_approach"]["openai_settings"]["n"]

        model = AzureChatOpenAI(
            openai_api_version=openai_api_version,
            azure_deployment=openai_deployment,
            azure_endpoint=self.__azure_openai_endpoint,
            api_key=self.__azure_openai_api_key,
            temperature=openai_temperature,
            max_tokens=openai_max_tokens,
            n=openai_n
        )
        
        system_prompt = dedent(chat_config["chat_approach"]["system_prompt"])
        
        if chat_config["chat_approach"]["documents"]["include"]:
            vector_store = self.generate_search(chat_config, openai_api_version)
            documents = vector_store.similarity_search(
            query=prompt,
                k=3,
                search_type="similarity",
            )

            if documents is not None and len(documents) > 0:
                system_prompt = "\nAdditional information:\n"
                
                for document in documents:
                    system_prompt += f"{document.page_content}\n"

        system_message = SystemMessage(content=dedent(system_prompt))

        message = HumanMessage(content=prompt)
        answer = model.invoke([system_message, message])
        chat_answer = Answer(formatted_answer=answer.content)

        return ChatResponse(answer=chat_answer)
    
    def generate_search(self, chat_config, openai_api_version) -> AzureSearch:
        azure_search_endpoint = self.__azure_search_endpoint
        azure_search_key = self.__azure_search_key
        index_name = chat_config["chat_approach"]["documents"]["index_name"]
        model = chat_config["chat_approach"]["documents"]["embedding_model"]
        embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
            openai_api_key=self.__azure_openai_api_key, 
            openai_api_version=openai_api_version, 
            azure_endpoint=self.__azure_openai_endpoint,
            model=model
        )
        
        return AzureSearch(
            azure_search_endpoint=azure_search_endpoint,
            azure_search_key=azure_search_key,
            index_name=index_name,
            embedding_function=embeddings.embed_query
        )