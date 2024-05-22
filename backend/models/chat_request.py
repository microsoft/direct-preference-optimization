"""This module contains the ChatRequest model."""
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Model for the chat request."""
    dialog: str
