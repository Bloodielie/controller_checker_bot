from typing import Callable

from aiogram import types
from state_manager import Depends
from state_manager.filters.base import BaseFilter
from state_manager.models.dependencys.aiogram import AiogramStateManager

from app.dependencies.locale import get_locale
from app.keybords.keybords import settings_keyboard


class SettingsFilter(BaseFilter):
    def __init__(self, func_with_raw_data: Callable):
        self.func_with_raw_data = func_with_raw_data

    async def check(self, msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale)) -> bool:  # type: ignore
        text = self.func_with_raw_data(locale)
        if msg.text.lower() in text:
            return True
        else:
            if msg.text.lower() == locale.back.lower():
                await state_manager.set_next_state("settings")
                await msg.answer(locale.settings_menu, reply_markup=settings_keyboard(locale))
                return False
            else:
                await msg.reply(locale.failed_settings)
                return False
