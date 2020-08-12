from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class User(BaseModel):
    id: int
    telegram_id: int
    username: str
    time_of_last_receipt: Optional[datetime]
    settings_id: int


class FullUser(BaseModel):
    id: int
    telegram_id: int
    username: str
    time_of_last_receipt: Optional[datetime]
    settings_id: int
    number_of_posts: int
    city: str
    representation: str
