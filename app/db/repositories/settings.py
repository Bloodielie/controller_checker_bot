from typing import Any

from app.db.models import settings
from app.db.repositories.base import BaseRepository


class SettingsRepository(BaseRepository):
    async def update_settings_by_id(self, id: int, **kwargs: Any) -> None:
        await self.db.execute(settings.update().where(settings.c.id == id).values(**kwargs))

    async def create(self, **values) -> int:
        return await self.db.execute(settings.insert(), values=values)
