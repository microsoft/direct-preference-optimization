"""This module contains the RateRequest model."""
from pydantic import BaseModel

class RateRequest(BaseModel):
    """Model for the rate request."""
    rating: bool
