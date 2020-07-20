from abc import ABC, abstractmethod
from asyncio import sleep
from typing import AsyncIterable, Type, List, Optional

from app.utils.vk_api import VkApiWrapper
from pydantic import BaseModel


class WallData(BaseModel):
    text: str
    date: int


class AbstractDataGetter(ABC):
    def __init__(self, vk_api: VkApiWrapper, last_bus_stop_time: Optional[int] = None) -> None:
        self.vk_api = vk_api
        self.last_bus_stop_time = last_bus_stop_time or 0

    @abstractmethod
    async def get_data(self, owner_id: int,) -> List[dict]:
        pass


class PostGetter(AbstractDataGetter):
    async def get_data(self, owner_id: int) -> List[dict]:
        return (await self.vk_api.method("wall.get", owner_id=owner_id, count=100)).get("items")


class PostInspector:
    def __init__(self, token: str, last_bus_stop_time: Optional[int] = None):
        self.vk_api = VkApiWrapper(token)
        self._last_bus_stop_time = last_bus_stop_time or 0

    async def check_data(
        self, owner_id: int, data_getter_class: Type[AbstractDataGetter], sleep_time: int = 150,
    ) -> AsyncIterable[WallData]:
        getter = data_getter_class(self.vk_api, self._last_bus_stop_time)

        while True:
            for item in (await getter.get_data(owner_id))[::-1]:
                date = item.get("date")
                if date > self._last_bus_stop_time:
                    self._last_bus_stop_time = date
                    yield WallData(text=item.get("text"), date=date)
                await sleep(0)
            await sleep(sleep_time)
