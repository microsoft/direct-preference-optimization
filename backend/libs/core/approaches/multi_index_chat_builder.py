"""This module contains the MultiIndexChatBuilder class
which is used to build a dynamic chat conversation"""

from textwrap import dedent

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from libs.core.models.options import MultiIndexVectorStoreOptions
from libs.core.services.search_vector_index_service import (
    search,
    generate_azure_search_client,
    generate_embeddings
)
from libs.core.services.sas_token_service import SasTokenService

class MultiIndexChatBuilder:
    """Class used to help build a dynamic chat conversation."""
    def __init__(
            self,
            multi_index_options: MultiIndexVectorStoreOptions
        ):
        self._primary_index_name = multi_index_options.primary_index_name
        self._secondary_index_name = multi_index_options.secondary_index_name
        self._vector_store_options = multi_index_options.vector_store_options
        self._open_ai_options = multi_index_options.open_ai_options
        self._storage_account_options = multi_index_options.storage_account_options
        self._token_service = SasTokenService(multi_index_options.storage_account_options)


    def llm(self):
        """Creates and returns an instance of a LLM class."""
        open_ai_options = self._open_ai_options
        api_options = open_ai_options.api_options
        model_options = open_ai_options.ai_model_options
        return AzureChatOpenAI(
            openai_api_version=api_options.api_version,
            azure_deployment=model_options.deployment_model,
            azure_endpoint=api_options.endpoint,
            api_key=api_options.api_key,
            temperature=model_options.temperature,
            max_tokens=model_options.max_tokens,
            n=model_options.n,
        )

    def chat_template(self, system_prompt):
        """Creates a chat template with a system message and a human message."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    dedent(system_prompt)
                ),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

    def _get_documents(self, index_name: str, query: str):
        embedding = generate_embeddings(self._open_ai_options)
        client = generate_azure_search_client(
            index_name = index_name,
            vector_store_options = self._vector_store_options,
            embedding_function = embedding)
        return search(client, query, 10)

    def get_primary_documents(self, question: str):
        """ Creating a new instance of the SearchVectorIndexService class with the 
            primary index name."""
        return self._get_documents(self._primary_index_name, question)

    def get_secondary_documents(self, question: str):
        """ Creating a new instance of the SearchVectorIndexService class with the 
            secondary index name."""
        return self._get_documents(self._secondary_index_name, question)

    def sort_and_filter_documents(self, _dict):
        """ Function for filtering and sorting documents based on their reranked scores.
            Using LangChain this could be split out into multiple runnables for better
            readability and maintainability."""
        primary_documents = _dict["primary_documents"]
        secondary_documents = _dict["secondary_documents"]
        documents = primary_documents + secondary_documents

        # Reverse sorting the documents based on the reranked score.
        documents = sorted(documents, key=lambda document: document[2], reverse=True)
        documents = documents[:3]
        return documents

    def format_docs(self, docs):
        """Function to format the documents into a string, with the URL included for citations"""
        formatted_docs = ""
        for d in docs:
            url = self._storage_account_options.url
            file_name = d[0].metadata["file_name"]
            container = d[0].metadata["container"]

            sas_token = self._token_service.get_sas_token_for_blob(file_name, container)
            formatted_docs += f'TITLE: {file_name}\n'
            formatted_docs += f'URL: {url}/{container}/{file_name}?{sas_token}'
            formatted_docs += f'CONTENT: {d[0].page_content}\n\n'
        return formatted_docs

    def default_return_message(self, default_return_message: str):
        """Function to return the default return message if no documents are found."""
        return AIMessage(default_return_message)
