from dataclasses import dataclass

@dataclass
class OpenAIOptions:
    """
    Options for configuring the OpenAI service.
    Args:
        endpoint: The OpenAI endpoint to use for chat.
    """
    endpoint: str
    api_key: str
    api_version: str
    deployment_model: str
    embedding_model: str
    temperature: float
    max_tokens: int
    n: int