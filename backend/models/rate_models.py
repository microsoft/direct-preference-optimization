"""This module contains the RateRequest model."""
from typing import List
from pydantic import BaseModel

class RateRequest(BaseModel):
    """Model for the rate request."""
    dialog_id: str
    rating: bool | None
    request: str
    response: str

class RateResponse(BaseModel):
    """Model for the rate response"""
    dialog_id: str
    output: List[str]
