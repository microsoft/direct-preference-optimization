from pydantic import BaseModel

class Chat(BaseModel):
    dialog: str