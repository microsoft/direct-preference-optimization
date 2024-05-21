from dataclasses import dataclass

@dataclass
class OpenAIOptions:
    """
    Options for configuring the OpenAI service.
    Args:
        endpoint: The OpenAI endpoint to use for chat conversation.
        api_key: The OpenAI api key to use when calling OpenAI.
        api_version: The OpenAI version of the endpoint.
        deployment_model: The model used for the chat conversation.
        embedding_model: The embedding model used for creating vectors for searching and storing content.
        temperature: Value used to control the randomness of the output.
        n: Number of chat completions to generate for each prompt.
    """
    endpoint: str
    api_key: str
    api_version: str
    deployment_model: str
    embedding_model: str
    temperature: float
    max_tokens: int
    n: int