from datetime import datetime
from typing import List

from PIL import ImageFont
from aiogram import types
from state_manager import Depends
from state_manager.models.dependencys.aiogram import AiogramStateManager
from state_manager.routes.aiogram import AiogramRouter

from app.config import PATH_TO_BASE_IMG, PATH_TO_BASE_FONT, y_cordinate, y_step, x_time_cordinate, x_message_cordinate, PATH_TO_IMAGES
from app.dependencies.locale import get_locale
from app.dependencies.user import get_user
from app.keybords.keybords import settings_keyboard
from app.models.bus_stop import BusStop
from app.models.settings import Representation
from app.models.user import Users
from app.utils.image import ImageWorker
from state_manager.utils.check import run_in_threadpool

other_state = AiogramRouter()


def draw_picture(bus_stops: List[BusStop], path_to_start_img: str, path_to_font: str, path_to_end_img: str) -> None:
    image_worker = ImageWorker(path_to_start_img)
    font = ImageFont.truetype(path_to_font, 34)
    cordinate_y = y_cordinate
    for bus_stop in bus_stops:
        message = bus_stop.message_text.replace("\n", "")
        if len(message) > 55:
            image_worker.text_drawing(x_message_cordinate, cordinate_y-20, f"{message[:55]}\n{message[55:110]}", (34, 34, 34), font)
        else:
            image_worker.text_drawing(x_message_cordinate, cordinate_y, message, (34, 34, 34), font)
        image_worker.text_drawing(x_time_cordinate, cordinate_y, str(bus_stop.created), (34, 34, 34), font)
        cordinate_y += y_step
    image_worker.save(path_to_end_img)


async def draw_and_send(msg: types.Message, bus_stops: List[BusStop], path_to_start_img: str, path_to_font: str, path_to_end_img: str):
    await run_in_threadpool(draw_picture, bus_stops, path_to_start_img, path_to_font,
                            f"{PATH_TO_IMAGES}/user_images.png")
    await msg.answer_photo(types.InputFile(path_to_end_img))


async def presentation_logic(user: Users, msg: types.Message, bus_stops: List[BusStop], locale) -> None:
    if not bus_stops:
        await msg.answer(locale.no_posts)
    elif user.settings.representation == Representation.photo:
        await Users.filter(telegram_id=msg.from_user.id).update(time_of_last_receipt=datetime.now())
        path_to_last_img = f"{PATH_TO_IMAGES}/user_images.png"
        if len(bus_stops) >= 14:
            for i in range(0, len(bus_stops), 14):
                if i == 0:
                    await draw_and_send(msg, bus_stops[:14], PATH_TO_BASE_IMG, PATH_TO_BASE_FONT, path_to_last_img)
                    continue
                await draw_and_send(msg, bus_stops[i:i+14], PATH_TO_BASE_IMG, PATH_TO_BASE_FONT, path_to_last_img)
        else:
            await draw_and_send(msg, bus_stops, PATH_TO_BASE_IMG, PATH_TO_BASE_FONT, path_to_last_img)
    elif user.settings.representation == Representation.text:
        string = ""
        for bus_stop in bus_stops:
            string += locale.new_posts.format(time=bus_stop.created, message=bus_stop.message_text)
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
