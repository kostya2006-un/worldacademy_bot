from datetime import datetime
from pydantic import BaseModel


class Topic(BaseModel):
    title: str
    id: int
