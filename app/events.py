import asyncio
from datetime import datetime
from typing import Type, Optional, Callable, Awaitable

from aiogram import Dispatcher
from databases import Database
from sqlalchemy import and_

from app.config import VK_API_TOKEN, BREST_GROUP_ID
from app.db.enum import City
from app.db.models import users, Representation, bus_stop
from app.db.repositories.settings import SettingsRepository
from app.db.repositories.user import UserRepository
from app.db.schemas.user import User
from app.utils.vk_getter import PostInspector, PostGetter, AbstractDataGetter


async def get_last_bus_stop_time(db: Database, city: City = City.brest) -> Optional[int]:
    last_bus_stop_time = await db.fetch_one(
        bus_stop.select().where(bus_stop.c.city == city.value).order_by(bus_stop.c.created.desc())
    )
    return int(last_bus_stop_time["created"].timestamp()) if last_bus_stop_time else None


async def scraper(
    db: Database, user: Type[User], group_id: int, vk_getter: Type[AbstractDataGetter], city: City = City.brest,
) -> None:
    last_bus_stop_time = await get_last_bus_stop_time(db, city)
    getter = PostInspector(VK_API_TOKEN, last_bus_stop_time)
    bus_stop_query = bus_stop.insert()
    async for wall_data in getter.check_data(group_id, vk_getter):
        text_lower = wall_data.text.lower()
        if "как" in text_lower or "где" in text_lower or not text_lower:
            continue
        await db.execute(
            bus_stop_query,
            values={
                "message_text": wall_data.text,
                "creator_id": user.id,
                "created": datetime.fromtimestamp(wall_data.date),
                "city": city.value,
            },
        )


def startup_wrapper(database: Database) -> Callable[[Dispatcher], Awaitable[None]]:
    async def startup(_) -> None:
        await database.connect()
        system_user = await UserRepository(database).default_executor(
            users.select().where(and_(users.c.id == 1, users.c.username == "system")), User
        )
        if system_user is None:
            settings_id = await SettingsRepository(database).create(
                number_of_posts=15, city=City.brest.value, representation=Representation.text.value
            )
            await database.execute(users.insert().values(username="system", telegram_id=1, settings_id=settings_id))

        asyncio.ensure_future(scraper(database, system_user, BREST_GROUP_ID, PostGetter, City.brest))

    return startup


def shutdown_wrapper(database: Database) -> Callable[[Dispatcher], Awaitable[None]]:
    async def shutdown(_) -> None:
        await database.disconnect()

    return shutdown
