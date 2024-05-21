"""Conversation logic for AI Chatbot."""

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
from services.search_vector_index_service import SearchVectorIndexServiceFactory

class ChatConversation:
    """Class used to manage the chat conversation
        and chain runnables together for the chat conversation"""

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
        self._factory = SearchVectorIndexServiceFactory()

    def get_primary_documents(self, query: str):
        """Get primary documents from the primary index."""
        vector_index_client = self._factory.generate_azure_search_client(
            self._primary_index_name,
            self._vector_store_options,
            self._open_ai_options)
        return vector_index_client.search(query, 10)

    def get_secondary_documents(self, query: str):
        """Get secondary documents from the secondary index."""
        vector_index_client = self._factory.generate_azure_search_client(
            self._secondary_index_name,
            self._vector_store_options,
            self._open_ai_options)
        return vector_index_client.search(query, 10)

    def sort_and_filter_documents(self, _dict):
        """Sort and filter the documents based on the reranked score."""
        # Function for filtering and sorting documents based on their reranked scores.
        # Using LangChain this could be split out into
        # multiple runnables for better readability and maintainability.
        primary_documents = _dict["primary_documents"]
        secondary_documents = _dict["secondary_documents"]
        documents = primary_documents + secondary_documents

        # Reverse sorting the documents based on the reranked score.
        documents = sorted(documents, key=lambda document: document[2], reverse=True)
        documents = documents[:3]
        return documents

    def format_docs(self, docs):
        """Format the documents to be passed to the AI model."""
        return "\n\n".join([d[0].page_content for d in docs])

def chat(conversation: ChatConversation,
        options: OpenAIOptions,
        system_prompt: str,
        prompt: str) -> ChatResponse:
    """Chat conversation with the AI model."""
    model = AzureChatOpenAI(
        openai_api_version=options.api_version,
        azure_deployment=options.deployment_model,
        azure_endpoint=options.endpoint,
        api_key=options.api_key,
        temperature=options.temperature,
        max_tokens=options.max_tokens,
        n=options.n,
    )

    # Creating a chat template with a system message and a human message.
    # Both messages are passed as templates.
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                dedent(system_prompt)
            ),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    # Creating a chain of runnables that will fill the context variable in the template.
    # Initially, this chain will get primary index documents
    # and append the secondary index documents to the list.
    # Then, it will sort and filter.
    chain = (
        {
            "context": {
                "primary_documents": itemgetter("question")
                    | RunnableLambda(conversation.get_primary_documents),
                "secondary_documents": itemgetter("question")
                    | RunnableLambda(conversation.get_secondary_documents),
            }
            | RunnableLambda(conversation.sort_and_filter_documents)
            | conversation.format_docs,
            "question": RunnablePassthrough(),
        }
        | chat_template
        | model
    )

    answer = chain.invoke({"question": prompt})
    chat_answer = Answer(formatted_answer=answer.content)

    return ChatResponse(answer=chat_answer)
