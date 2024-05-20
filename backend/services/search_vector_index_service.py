from typing import List, Tuple

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_core.documents import Document

from models.vector_store_options import VectorStoreOptions
from models.openai_options import OpenAIOptions

class SearchVectorIndexService:
    def __init__(self, index_name: str, vector_store_options: VectorStoreOptions, open_ai_options: OpenAIOptions):
        embeddings = self._generate_embeddings(open_ai_options)
        self._vector_search_client = self._generate_azure_search_client(index_name, vector_store_options, embeddings)

    def search(
        self, query: str, numberOfResults: int
    ) -> List[Tuple[Document, float, float]]:
        documents = (
            self._vector_search_client.semantic_hybrid_search_with_score_and_rerank(
                query=query, k=numberOfResults
            )
        )

        return documents

    def _generate_embeddings(self, open_ai_options: OpenAIOptions) -> AzureOpenAIEmbeddings:
        return AzureOpenAIEmbeddings(
            openai_api_key=open_ai_options.api_key,
            openai_api_version=open_ai_options.api_version,
            azure_endpoint=open_ai_options.endpoint,
            model=open_ai_options.embedding_model,
        )

    def _generate_azure_search_client(self, index_name: str, vector_store_options: VectorStoreOptions, embedding_function: List[float]) -> AzureSearch:
        return AzureSearch(
            azure_search_endpoint=vector_store_options.endpoint,
            azure_search_key=vector_store_options.key,
            index_name=index_name,
            embedding_function=embedding_function,
            semantic_configuration_name=vector_store_options.semantic_configuration_name,
        )