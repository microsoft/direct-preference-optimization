"""Service class for searching the vector index."""

from typing import List, Tuple

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_core.documents import Document

from libs.core.models.vector_store_options import VectorStoreOptions
from libs.core.models.openai_options import OpenAIOptions
from models.rate_models import RateResponse, RateRequest

def generate_embeddings(open_ai_options: OpenAIOptions) -> AzureOpenAIEmbeddings:
    """Generate the Azure OpenAI embeddings."""
    api_options = open_ai_options.api_options
    model_options = open_ai_options.model_options
    return AzureOpenAIEmbeddings(
        openai_api_key=api_options.api_key,
        openai_api_version=api_options.api_version,
        azure_endpoint=api_options.endpoint,
        model=model_options.embedding_model,
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
    return client.semantic_hybrid_search_with_score_and_rerank(
        query=query, k=number_of_results)

def rate(
    client: AzureSearch,
    rate_request: RateRequest) -> dict:
    """Rate the conversation."""
    output = client.add_texts(
        texts=[rate_request.response],
        labels=[{
            True: "rating:thumbs-up",
            False: "rating:thumbs-down",
            None: "rating:none"}
            [rate_request.rating]],
        metadata={"rating": rate_request.rating})

    return RateResponse(
        dialog_id = rate_request.dialog_id,
        output = output
    )
