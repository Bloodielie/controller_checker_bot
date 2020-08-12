from datetime import datetime
from typing import Any, List, TypeVar, Optional, Type

from app.db.models import bus_stop
from app.db.repositories.base import BaseRepository
from app.db.schemas.bus_stop import BusStop

T = TypeVar("T")


class BusStopRepository(BaseRepository):
    async def default_executor(self, query) -> List[BusStop]:
        result = []
        async for row in self.db.iterate(query=query):
            result.append(BusStop.parse_obj({**row}))
        return result

    async def get_bus_stop_by_city(self, city: str, limit: int = 15) -> List[BusStop]:
        query = bus_stop.select().where(bus_stop.c.city == city).order_by(bus_stop.c.created.desc()).limit(limit)
        return await self.default_executor(query)

    async def get_bus_stop_by_created(self, created: datetime, limit: int = 15) -> List[BusStop]:
        query = bus_stop.select().where(bus_stop.c.created >= created).order_by(bus_stop.c.created.desc()).limit(limit)
        return await self.default_executor(query)

    # async def update_settings_by_id(self, id: int, **kwargs: Any) -> None:
    #    await self.db.execute(settings.update().where(settings.c.id == id).values(**kwargs))

    # async def create(self, **values) -> int:
    #    return await self.db.execute(settings.insert(), values=values)
