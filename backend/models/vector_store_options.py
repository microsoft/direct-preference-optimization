from dataclasses import dataclass

@dataclass
class VectorStoreOptions:
    endpoint: str
    key: str
    semantic_configuration_name: str