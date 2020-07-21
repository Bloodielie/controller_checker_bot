from inspect import isfunction
from typing import Callable, Union, List

from aiogram import types
from state_manager import Depends
from state_manager.filters.base import BaseFilter
from state_manager.models.dependencys.aiogram import AiogramStateManager

from app.dependencies.locale import get_locale
from app.keybords.keybords import settings_keyboard


class SettingsFilter(BaseFilter):
    def __init__(self, raw_data: Union[Callable, list]):
        self.raw_data = raw_data

    async def check(self, msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale)) -> bool:  # type: ignore
        text = self.check_raw_data(locale)
        if msg.text.lower() in text:
            return True
        else:
            if msg.text.lower() == locale.back.lower():
                await state_manager.back_to_pre_state()
                await msg.answer(locale.settings_menu, reply_markup=settings_keyboard(locale))
                return False
            else:
                await msg.reply(locale.failed_representation_msg)
                return False

    def check_raw_data(self, locale) -> List[str]:
        if isfunction(self.raw_data):
            return [text.lower() for text in self.raw_data(locale)]
        elif isinstance(self.raw_data, list):
            return self.raw_data
        else:
            raise TypeError()
