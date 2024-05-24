"""Chat Response models."""

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from langchain.docstore.document import Document

from libs.core.models.storage_account_options import StorageAccountOptions

class ApproachType(Enum):
    """Enum for the approach type."""
    STRUCTURED = "1"
    UNSTRUCTURED = "2"
    CHIT_CHAT = "3"
    CONTINUATION = "4"
    INAPPROPRIATE = "5"

@dataclass
class AnswerQueryConfig:
    """Model for the answer query configuration."""
    def __init__(
        self,
        query_generation_prompt: Optional[str] = None,
        query: Optional[str] = None,
        query_result: Optional[str] = None,
    ):
        self.query_generation_prompt = query_generation_prompt
        self.query = query
        self.query_result = query_result

@dataclass
class Answer:
    """Model for the answer."""
    def __init__(
        self,
        formatted_answer: str = "",
        citations: dict = None,
        answer_query_config: Optional[AnswerQueryConfig] = None,
    ):
        self.formatted_answer = formatted_answer
        if citations is None:
            citations = {}
        self.citations = citations
        self.query_generation_prompt = answer_query_config.query_generation_prompt
        self.query = answer_query_config.query
        self.query_result = answer_query_config.query_result

def to_answer_item(answer: Answer):
    """Returns a formatted item for the answer."""
    answer_item = {
        "formatted_answer": answer.formatted_answer,
        "citations": list(map(lambda citation: citation.to_dict(), answer.citations)),
        "query_generation_prompt": answer.query_generation_prompt,
        "query": answer.query,
        "query_result": answer.query_result,
    }
    return answer_item

@dataclass
class ChatResponseArgs:
    """Model for the chat response arguments."""
    def __init__(
        self,
        classification: Optional[ApproachType] = None,
        data_points: List[str] = None,
        error: Optional[str] = None,
        suggested_classification: Optional[ApproachType] = None,
    ):
        self.classification = classification
        self.data_points = [] if data_points is None else data_points
        self.error = error
        self.suggested_classification = suggested_classification

@dataclass
class ChatResponse:
    """Model for the chat response."""
    def __init__(
        self,
        answer: Answer,
        chat_response_args: Optional[ChatResponseArgs] = None,
        show_retry: bool = False,
    ):
        self.answer = answer
        self.classification = chat_response_args.classification
        self.data_points = ([]
            if chat_response_args.data_points is None
            else chat_response_args.data_points)
        self.error = chat_response_args.error
        self.suggested_classification = chat_response_args.suggested_classification
        self.show_retry = show_retry

def to_response_item(response: ChatResponse):
    """Returns a formatted item for the chat response."""
    return {
        "classification": (
            response.classification.name if response.classification is not None else None
        ),
        "answer": to_answer_item(response.answer),
        "data_points": [str(data_point) for data_point in response.data_points],
        "error": response.error,
        "suggested_classification": (
            response.suggested_classification.value
            if response.suggested_classification is not None
            else None
        ),
        "show_retry": response.show_retry,
    }

@dataclass
class Citation:
    """Model for the citation."""
    def __init__(
        self,
        document_id: str = "",
        document_title: str = "",
        document_url: str = "",
        document_snippet: str = "",
    ):
        self.document_id = document_id
        self.document_title = document_title
        self.document_url = document_url
        self.document_snippet = document_snippet

    def to_dict(self):
        """Returns a dictionary representation of the citation."""
        return {
            "document_id": self.document_id,
            "document_title": self.document_title,
            "document_url": self.document_url,
            "document_snippet": self.document_snippet,
        }

def citation_from_formatted_doc(stg_acct_opts: StorageAccountOptions, doc: Document):
    """Creates a Citation from a formatted document."""
    metadata = doc[0].metadata
    return Citation(
        document_id=metadata["document_id"],
        document_title=metadata["file_name"],
        document_url=f'{stg_acct_opts.url}/{metadata["container"]}/{metadata["file_name"]}',
        document_snippet=metadata["captions"]["highlights"]
    )
