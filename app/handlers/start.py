from aiogram import types
from state_manager import Depends
from state_manager.models.dependencys.aiogram import AiogramStateManager
from state_manager.routes.aiogram import AiogramRouter

from app.db.enum import City, Representation
from app.db.repositories.settings import SettingsRepository
from app.db.repositories.user import UserRepository
from app.depends import get_locale
from app.keybords.keybords import start_keyboard, representation_keyboard, menu_keyboard
from app.keybords.raw_text import city_raw_text, representation_raw_text
from app.utils.utils import find_value_in_enum

start_state = AiogramRouter()


@start_state.message_handler()
async def start(
    msg: types.Message,
    state_manager: AiogramStateManager,
    user_rep: UserRepository,
    settings_rep: SettingsRepository,
    locale=Depends(get_locale),
):
    user_obj = msg.from_user
    if not await user_rep.exist(user_obj.id):
        settings_id = await settings_rep.create(
            number_of_posts=15, city=City.brest.value, representation=Representation.text.value
        )
        await user_rep.create(telegram_id=user_obj.id, username=(user_obj.username or "NONE"), settings_id=settings_id)
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
    msg: types.Message, state_manager: AiogramStateManager, user_rep: UserRepository, locale=Depends(get_locale)
):
    if msg.text.lower() in [text.lower() for text in representation_raw_text(locale)]:
        city = (await state_manager.data)["city"]
        representation = find_value_in_enum(msg.text, Representation, locale)
        await user_rep.update_settings_by_telegram_id(telegram_id=msg.from_user.id, city=city, representation=representation)

        await state_manager.set_next_state("main_menu")
        await msg.answer(locale.main_menu, reply_markup=menu_keyboard(locale))
    else:
        await msg.reply(
            locale.failed_representation_msg, reply_markup=representation_keyboard(locale),
        )
