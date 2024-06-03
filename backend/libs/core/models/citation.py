from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

class Citation(BaseModel):
    source_id: int = Field(
        ...,
        description="The integer ID of a SPECIFIC source which justifies the answer.",
    )
    url: str = Field(
        ...,
        description="The URL of the source.",
    )
    title: str = Field(
        ...,
        description="A short title of the source.",
    )
    page_number: int = Field(
        ...,
        description="The page number of the source that justifies the answer.",
    )