from aiogram import types
from state_manager import Depends
from state_manager.models.dependencys.aiogram import AiogramStateManager
from state_manager.routes.aiogram import AiogramRouter

from app.dependencies.locale import get_locale
from app.dependencies.user import get_user
from app.keybords.keybords import start_keyboard, representation_keyboard, menu_keyboard
from app.keybords.raw_text import city_raw_text, representation_raw_text
from app.models.settings import Settings, Representation, City
from app.utils.utils import find_value_in_enum

start_state = AiogramRouter()


@start_state.message_handler()
async def start(msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale)):
    await state_manager.set_next_state("city_choice")
    await msg.reply(locale.start_msg, reply_markup=start_keyboard(locale))


@start_state.message_handler()
async def city_choice(msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale)):
    lower_text = msg.text.lower()
    if lower_text in [text.lower() for text in city_raw_text(locale)]:
        city = find_value_in_enum(msg.text, City, locale)
        await state_manager.set_next_state("representation_choice", data={"city": city})
        await msg.reply(locale.representation_msg, reply_markup=representation_keyboard(locale))
    else:
        await msg.reply(locale.failed_start_msg, reply_markup=start_keyboard(locale))


@start_state.message_handler()
async def representation_choice(
    msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale), user=Depends(get_user),
):
    lower_text = msg.text.lower()
    if lower_text in [text.lower() for text in representation_raw_text(locale)]:
        city = (await state_manager.data)["city"]
        representation = find_value_in_enum(msg.text, Representation, locale)
        await Settings.filter(id=user.settings.id).update(city=city, representation=representation)
        await state_manager.set_next_state("main_menu")
        await msg.answer(locale.main_menu, reply_markup=menu_keyboard(locale))
    else:
        await msg.reply(
            locale.failed_representation_msg, reply_markup=representation_keyboard(locale),
        )
