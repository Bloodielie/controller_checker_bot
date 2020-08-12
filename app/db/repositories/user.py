from typing import Optional, TypeVar, Union

from sqlalchemy import select

from app.db.models import users, settings
from app.db.repositories.base import BaseRepository
from app.db.schemas.user import User, FullUser

T = TypeVar("T")


class UserRepository(BaseRepository):
    async def default_executor(self, query, model: T, fetch_type: str = "fetch_one") -> Optional[T]:
        fetch = getattr(self.db, fetch_type)
        data = await fetch(query)
        if data is None:
            return None
        return model.parse_obj({**data})

    async def get_user_by_telegram_id(self, telegram_id: int, *, is_full: bool = False) -> Optional[Union[User, FullUser]]:
        if not is_full:
            query = users.select().where(users.c.telegram_id == telegram_id)
            return await self.default_executor(query, User)
        else:
            query = select([users, settings]).where(users.c.telegram_id == telegram_id).select_from(users.outerjoin(settings))
            return await self.default_executor(query, FullUser)

    async def create(self, **values) -> int:
        return await self.db.execute(users.insert(), values=values)

    async def exist(self, telegram_id: int) -> bool:
        user = await self.get_user_by_telegram_id(telegram_id)
        return True if user is not None else False

    async def update_settings_by_telegram_id(self, telegram_id: int, **data_to_update) -> None:
        query = (
            settings.update()
            .values(**data_to_update)
            .where(settings.c.id == select([users.c.settings_id]).where(users.c.telegram_id == telegram_id))
        )
        return await self.db.execute(query)

    async def update(self, telegram_id: int, **data_to_update) -> None:
        query = users.update().values(**data_to_update).where(users.c.telegram_id == telegram_id)
        return await self.db.execute(query)
