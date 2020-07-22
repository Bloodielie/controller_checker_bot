import logging
import os
import sys

from state_manager import RedisStorage
from state_manager.storage_settings import StorageSettings

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.split(dir_path)[0])

from aiogram import Bot, Dispatcher, executor

from state_manager.routes.aiogram import AiogramMainRouter

from app.config import TELEGRAM_API_TOKEN
from app.events import shutdown, startup
from app.handlers.other import other_state
from app.handlers.settings import settings_state
from app.handlers.start import start_state
from app.middlewares.locales import LocaleMiddleware
from app.middlewares.new_user import NewUserMiddleware
from app.middlewares.spam import AntiSpamMiddleware

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LocaleMiddleware("./localization"))
dp.middleware.setup(AntiSpamMiddleware(limit=30, delay=30))
dp.middleware.setup(NewUserMiddleware())

main_state = AiogramMainRouter(dp)
main_state.include_router(start_state)
main_state.include_router(other_state)
main_state.include_router(settings_state)
main_state.install(default_state_name="start")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
