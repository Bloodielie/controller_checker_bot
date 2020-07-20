import asyncio
from datetime import datetime
from typing import Type, Optional

from tortoise import Tortoise

from app.config import VK_API_TOKEN, BREST_GROUP_ID, TORTOISE_ORM
from app.models.bus_stop import BusStop
from app.models.settings import Settings, City
from app.models.user import Users
from app.utils.vk_getter import PostInspector, PostGetter, AbstractDataGetter


async def get_last_bus_stop_time(city: City = City.brest) -> Optional[int]:
    last_bus_stop_time = await BusStop.filter(city=city).order_by("-id").limit(1)
    return int(last_bus_stop_time[0].created.timestamp()) if last_bus_stop_time else None


async def scraper(user: Users, group_id: int, vk_getter: Type[AbstractDataGetter], city: City = City.brest,) -> None:
    last_bus_stop_time = await get_last_bus_stop_time(city)
    getter = PostInspector(VK_API_TOKEN, last_bus_stop_time)
    async for wall_data in getter.check_data(group_id, vk_getter):
        text_lower = wall_data.text.lower()
        if "как" in text_lower or "где" in text_lower or not text_lower:
            continue
        await BusStop.create(
            message_text=wall_data.text, creator=user, created=datetime.fromtimestamp(wall_data.date), city=city,
        )


async def startup(dp):
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    system_user = await Users.filter(username="system", telegram_id=1).first()
    if system_user is None:
        system_user = await Users.create(username="system", telegram_id=1, settings=await Settings.create())

    asyncio.ensure_future(scraper(system_user, BREST_GROUP_ID, PostGetter, City.brest))


async def shutdown(dp):
    await Tortoise.close_connections()
