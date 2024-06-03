from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from libs.core.models.citation import Citation

class CitedAnswer(BaseModel):
    """Answer the user question based only on the given sources, and cite the sources used."""

    answer: str = Field(
        ...,
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: List[Citation] = Field(
        ..., 
        description="Citations from the given sources that justify the answer."
    )