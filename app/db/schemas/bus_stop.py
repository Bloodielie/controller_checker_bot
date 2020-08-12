from pydantic import BaseModel
from datetime import datetime


class BusStop(BaseModel):
    id: int
    message_text: str
    city: str
    created: datetime
    creator_id: int
