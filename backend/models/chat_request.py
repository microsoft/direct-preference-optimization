"""This module contains the ChatRequest model."""
from pydantic import BaseModel

class Chat(BaseModel):
    """Model for the chat request."""
    dialog: str
