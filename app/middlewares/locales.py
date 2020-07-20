from typing import Optional

import state_manager

try:
    import ujson as json
except ImportError:
    import json

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiofiles import open
from dataclasses import make_dataclass


class LocaleMiddleware(BaseMiddleware):
    def __init__(self, path_to_locale: str, is_cached: bool = True, default_lang: str = "ru"):
        super().__init__()
        self.path_to_locale = path_to_locale
        self.is_cached = is_cached
        self._cache = {}
        self.default_lang = default_lang

    async def load_locales(self, ctx: state_manager.types.Context, data: dict):
        locale_lang = str(ctx.from_user.locale)
        if self.is_cached:
            locale = self._cache.get(locale_lang)
            if locale is not None:
                data["locale"] = locale
                return

        locale = await self.get_data_in_file(locale_lang)
        if locale is None:
            locale = await self.get_data_in_file(self.default_lang)
        locale_obj = make_dataclass(f"Locale{locale_lang.capitalize()}", locale.keys())(*locale.values())
        data["locale"] = locale_obj
        self._cache[locale_lang] = locale_obj

    async def get_data_in_file(self, locale: str) -> Optional[dict]:
        try:
            async with open(f"{self.path_to_locale}/{locale}.json", "r", encoding="utf-8") as f:
                return json.loads(await f.read())
        except FileNotFoundError:
            return None

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        await self.load_locales(message, data)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict) -> None:
        await self.load_locales(query, data)
