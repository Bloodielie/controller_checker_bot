import asyncio
from typing import Dict, Optional, Any

import aiohttp


class VkApiWrapper:
    def __init__(
        self,
        token: str,
        *,
        api_version: str = "5.92",
        session: Optional[aiohttp.ClientSession] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        vk_api_url: Optional[str] = None,
    ) -> None:
        self._default_params = {"access_token": token, "v": api_version}
        self._loop = loop or asyncio.get_event_loop()
        self._session = session or aiohttp.ClientSession(loop=self._loop)
        self._vk_api_url = vk_api_url or "https://api.vk.com/method"

    @property
    def get_default_params(self) -> dict:
        return self._default_params

    @get_default_params.setter
    def get_default_params(self, value: Dict[str, Any]) -> None:
        if not value.get("access_token") and not value.get("v"):
            raise TypeError("In default parameters there should be a token and version")
        self._default_params = value

    async def method(self, method: str, **kwargs: Any) -> dict:
        async with self._session.get(f"{self._vk_api_url}/{method}", params={**self._default_params, **kwargs}) as response:
            response = await response.json()
            error = response.get("error")
            if error:
                raise Exception(f"Vk api error: {error}")
            return response.get("response")

    async def close(self) -> None:
        await self._session.close()
