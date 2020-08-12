from datetime import datetime

from aiogram import types
from state_manager import Depends
from state_manager.models.dependencys.aiogram import AiogramStateManager
from state_manager.routes.aiogram import AiogramRouter

from app.db.enum import Representation
from app.db.repositories.bus_stop import BusStopRepository
from app.db.repositories.user import UserRepository
from app.depends import get_locale
from app.keybords.keybords import settings_keyboard
from app.services.bus_stop import BusStopService

other_state = AiogramRouter()


@other_state.message_handler()
async def main_menu(
    msg: types.Message,
    state_manager: AiogramStateManager,
    user_rep: UserRepository,
    bus_stop_rep: BusStopRepository,
    service: BusStopService,
    locale=Depends(get_locale),
):
    lower_text = msg.text.lower()
    if lower_text == locale.get_updates.lower():
        user = await user_rep.get_user_by_telegram_id(msg.from_user.id, is_full=True)
        if user.time_of_last_receipt is None:
            bus_stops = await bus_stop_rep.get_bus_stop_by_city(user.city, user.number_of_posts)
        else:
            bus_stops = await bus_stop_rep.get_bus_stop_by_created(user.time_of_last_receipt, user.number_of_posts)
        await user_rep.update(msg.from_user.id, time_of_last_receipt=datetime.now())

        if not bus_stops:
            await msg.answer(locale.no_posts)
        elif user.representation == Representation.photo:
            async for picture_bytes in service.get_pictures(bus_stops):
                await msg.answer_photo(picture_bytes)
        elif user.representation == Representation.text:
            text = service.generate_view_text(bus_stops)
            await msg.answer(text, parse_mode="html")
    elif lower_text == locale.settings.lower():
        await state_manager.set_next_state("settings")
        await msg.answer(locale.settings_menu, reply_markup=settings_keyboard(locale))
