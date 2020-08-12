import io
from typing import List, AsyncIterator

from PIL import ImageFont
from state_manager import Depends
from state_manager.utils.utils import run_in_threadpool

from app.config import PATH_TO_BASE_IMG, PATH_TO_BASE_FONT, y_cordinate, x_message_cordinate, x_time_cordinate, y_step
from app.db.schemas.bus_stop import BusStop
from app.depends import get_locale
from app.utils.image import ImageWorker


class BusStopService:
    def __init__(self, locale=Depends(get_locale)):
        self._locale = locale

    def generate_view_text(self, bus_stops: List[BusStop]):
        string = ""
        for bus_stop in bus_stops:
            string += self._locale.new_posts.format(time=bus_stop.created, message=bus_stop.message_text)
        return string

    async def get_pictures(self, bus_stops: List[BusStop]) -> AsyncIterator[io.BytesIO]:
        if len(bus_stops) >= 14:
            for i in range(0, len(bus_stops), 14):
                if i == 0:
                    yield await run_in_threadpool(self.get_picture, bus_stops[:14])
                else:
                    yield await run_in_threadpool(self.get_picture, bus_stops[i:i + 14])
        else:
            yield await run_in_threadpool(self.get_picture, bus_stops)

    @staticmethod
    def get_picture(bus_stops: List[BusStop]) -> bytes:
        image_worker = ImageWorker(PATH_TO_BASE_IMG)
        font = ImageFont.truetype(PATH_TO_BASE_FONT, 34)
        cordinate_y = y_cordinate

        for bus_stop in bus_stops:
            message = bus_stop.message_text.replace("\n", "")
            if len(message) > 55:
                image_worker.text_drawing(
                    x_message_cordinate, cordinate_y - 20, f"{message[:55]}\n{message[55:110]}", (34, 34, 34), font
                )
            else:
                image_worker.text_drawing(x_message_cordinate, cordinate_y, message, (34, 34, 34), font)
            image_worker.text_drawing(x_time_cordinate, cordinate_y, str(bus_stop.created), (34, 34, 34), font)
            cordinate_y += y_step

        img_byte_list = io.BytesIO()
        image_worker.transparent.save(img_byte_list, format='gif')
        return img_byte_list.getvalue()
