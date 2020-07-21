from aiogram import types
from state_manager import Depends
from state_manager.models.dependencys.aiogram import AiogramStateManager
from state_manager.routes.aiogram import AiogramRouter

from app.dependencies.locale import get_locale
from app.dependencies.user import get_user
from app.filters.settings import SettingsFilter
from app.keybords.keybords import (
    menu_keyboard,
    settings_city_keyboard,
    settings_representation_keyboard,
    settings_number_of_posts_keyboard,
)
from app.keybords.raw_text import city_raw_text, representation_raw_text, number_of_posts_raw_text
from app.models.settings import City, Settings, Representation
from app.utils.utils import find_value_in_enum

settings_state = AiogramRouter()


@settings_state.message_handler()
async def settings(msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale)):
    lower_text = msg.text.lower()
    if lower_text == locale.settings_city.lower():
        await state_manager.set_next_state("settings_city")
        await msg.answer(locale.settings_city_msg, reply_markup=settings_city_keyboard(locale))
    elif lower_text == locale.settings_representation.lower():
        await state_manager.set_next_state("settings_representation")
        await msg.answer(locale.settings_representation_msg, reply_markup=settings_representation_keyboard(locale))
    elif lower_text == locale.settings_number_of_posts.lower():
        await state_manager.set_next_state("settings_number_of_posts")
        await msg.answer(locale.settings_number_of_posts_msg, reply_markup=settings_number_of_posts_keyboard(locale))
    elif lower_text == locale.back.lower():
        await state_manager.set_next_state("main_menu")
        await msg.answer(locale.main_menu, reply_markup=menu_keyboard(locale))


@settings_state.message_handler(SettingsFilter(city_raw_text))
async def settings_city(
    msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale), user=Depends(get_user)
):
    city = find_value_in_enum(msg.text, City, locale)
    await Settings.filter(id=user.settings.id).update(city=city)
    await state_manager.set_next_state("main_menu")
    await msg.answer(locale.main_menu, reply_markup=menu_keyboard(locale))


@settings_state.message_handler(SettingsFilter(representation_raw_text))
async def settings_representation(
    msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale), user=Depends(get_user)
):
    representation = find_value_in_enum(msg.text, Representation, locale)
    await Settings.filter(id=user.settings.id).update(representation=representation)
    await state_manager.set_next_state("main_menu")
    await msg.answer(locale.main_menu, reply_markup=menu_keyboard(locale))


@settings_state.message_handler(SettingsFilter(number_of_posts_raw_text))
async def settings_number_of_posts(
    msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale), user=Depends(get_user)
):
    await Settings.filter(id=user.settings.id).update(number_of_posts=int(msg.text.lower()))
    await state_manager.set_next_state("main_menu")
    await msg.answer(locale.main_menu, reply_markup=menu_keyboard(locale))
