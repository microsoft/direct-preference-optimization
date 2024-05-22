"""Service class for searching the vector index."""

from typing import List, Tuple

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_core.documents import Document

from models.vector_store_options import VectorStoreOptions
from models.openai_options import OpenAIOptions

def generate_embeddings(open_ai_options: OpenAIOptions) -> AzureOpenAIEmbeddings:
    """Generate the Azure OpenAI embeddings."""
    return AzureOpenAIEmbeddings(
        openai_api_key=open_ai_options.api_key,
        openai_api_version=open_ai_options.api_version,
        azure_endpoint=open_ai_options.endpoint,
        model=open_ai_options.embedding_model,
    )

def generate_azure_search_client(
    index_name: str,
    vector_store_options: VectorStoreOptions,
    embedding_function: List[float]) -> AzureSearch:
    """Generate the Azure Search client."""
    return AzureSearch(
        azure_search_endpoint=vector_store_options.endpoint,
        azure_search_key=vector_store_options.key,
        index_name=index_name,
        embedding_function=embedding_function,
        semantic_configuration_name=vector_store_options.semantic_configuration_name,
    )

def search(
    client: AzureSearch,
    query: str, number_of_results: int
) -> List[Tuple[Document, float, float]]:
    """Search the vector index and return the document scores / reranked values."""
    return (
        client.semantic_hybrid_search_with_score_and_rerank(
            query=query, k=number_of_results
        )
    )
