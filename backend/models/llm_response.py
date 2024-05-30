from dataclasses import dataclass
from models.chat_response import Citation

@dataclass
class LlmResponse:
    answer: str
    citations: list[Citation]
    