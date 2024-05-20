from dataclasses import dataclass

@dataclass
class VectorStoreOptions:
    """
    Options for configuring the vector store service.
    Args:
        endpoint: The vector store endpoint to use for retrieving documents.
        key: The vector store key to use when calling the service.
        semantic_configuration_name: The semantic configuration name used in the portal to describe the fields used for reranking.
    """
    endpoint: str
    key: str
    semantic_configuration_name: str