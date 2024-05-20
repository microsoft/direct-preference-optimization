from textwrap import dedent
from operator import itemgetter

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import (RunnablePassthrough, RunnableLambda)

from models.chat_response import Answer
from models.chat_response import ChatResponse
from models.vector_store_options import VectorStoreOptions
from models.openai_options import OpenAIOptions
from services.search_vector_index_service import SearchVectorIndexService


class ChatConversation:

    def __init__(
            self,
            primary_index_name: str,
            secondary_index_name: str,
            vector_store_options: VectorStoreOptions,
            open_ai_options: OpenAIOptions
        ):
        self._primary_index_name = primary_index_name
        self._secondary_index_name = secondary_index_name
        self._vector_store_options = vector_store_options
        self._open_ai_options = open_ai_options


    def _get_gardening_documents(self, query: str):
        vector_index_client = SearchVectorIndexService(self._primary_index_name, self._vector_store_options, self._open_ai_options)

        return vector_index_client.search(query, 10)


    def _get_aca_documents(self, query: str):
        vector_index_client = SearchVectorIndexService(self._secondary_index_name, self._vector_store_options, self._open_ai_options)
        return vector_index_client.search(query, 10)


    def _sort_and_filter_documents(self, _dict):
        garden_documents = _dict["aca_documents"]
        aca_documents = _dict["garden_documents"]
        documents = garden_documents + aca_documents

        documents = [document for document in documents if document[2] >= 3]
        documents = sorted(documents, key=lambda document: document[2], reverse=True)
        documents = documents[:5]

        return documents

    def chat(self, system_prompt: str, prompt: str) -> ChatResponse:
        model = AzureChatOpenAI(
            openai_api_version=self._open_ai_options.api_version,
            azure_deployment=self._open_ai_options.deployment_model,
            azure_endpoint=self._open_ai_options.endpoint,
            api_key=self._open_ai_options.api_key,
            temperature=self._open_ai_options.temperature,
            max_tokens=self._open_ai_options.max_tokens,
            n=self._open_ai_options.n,
        )

        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    dedent(system_prompt)
                ),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
        
        chain = (
            {
                "context": {
                    "garden_documents": itemgetter("question")
                    | RunnableLambda(self._get_gardening_documents),
                    "aca_documents": itemgetter("question") | RunnableLambda(self._get_aca_documents),
                }
                | RunnableLambda(self._sort_and_filter_documents),
                "question": RunnablePassthrough(),
            }
            | chat_template
            | model
        )
        answer = chain.invoke({"question": prompt})
        chat_answer = Answer(formatted_answer=answer.content)

        return ChatResponse(answer=chat_answer)
