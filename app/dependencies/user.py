from typing import Optional

from app.models.user import Users


def get_user(data: dict) -> Optional[Users]:
    return data.get("user")
