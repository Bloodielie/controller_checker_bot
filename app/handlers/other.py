from datetime import datetime
from typing import List

from aiogram import types
from state_manager import Depends
from state_manager.models.dependencys.aiogram import AiogramStateManager
from state_manager.routes.aiogram import AiogramRouter

from app.dependencies.locale import get_locale
from app.dependencies.user import get_user
from app.keybords.keybords import settings_keyboard
from app.models.bus_stop import BusStop
from app.models.settings import Representation
from app.models.user import Users

other_state = AiogramRouter()


async def presentation_logic(user: Users, msg: types.Message, bus_stops: List[BusStop], locale):
    if user.settings.representation == Representation.photo:
        await msg.answer(locale.photo_no_support)
        return
    elif user.settings.representation == Representation.text:
        string = ""
        for bus_stop in bus_stops:
            string += locale.new_posts.format(time=bus_stop.created, message=bus_stop.message_text)
        if not string:
            await msg.answer(locale.no_posts)
        else:
            await msg.answer(string, parse_mode="html")
    await Users.filter(telegram_id=msg.from_user.id).update(time_of_last_receipt=datetime.now())


@other_state.message_handler()
async def main_menu(
    msg: types.Message, state_manager: AiogramStateManager, locale=Depends(get_locale), user: Users = Depends(get_user),
):
    lower_text = msg.text.lower()
    if lower_text == locale.get_updates.lower():
        if user.time_of_last_receipt is None:
            bus_stops = await BusStop.filter(city=user.settings.city).order_by("-created").limit(user.settings.number_of_posts)
            await presentation_logic(user, msg, bus_stops, locale)
        else:
            bus_stops = (
                await BusStop.filter(created__gt=user.time_of_last_receipt)
                .order_by("-created")
                .limit(user.settings.number_of_posts)
            )
            await presentation_logic(user, msg, bus_stops, locale)
    elif lower_text == locale.settings.lower():
        await state_manager.set_next_state("settings")
        await msg.answer(locale.settings_menu, reply_markup=settings_keyboard(locale))
