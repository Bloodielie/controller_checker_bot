import logging
import os
import sys

from state_manager import MemoryStorage

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.split(dir_path)[0])

from app.db.repositories.bus_stop import BusStopRepository
from app.db.repositories.settings import SettingsRepository
from app.db.repositories.user import UserRepository
from app.services.bus_stop import BusStopService

from aiogram import Bot, Dispatcher, executor

from state_manager.routes.aiogram import AiogramMainRouter

from app.config import TELEGRAM_API_TOKEN, DB_URL
from app.events import startup_wrapper, shutdown_wrapper

from app.handlers.other import other_state
from app.handlers.settings import settings_state
from app.handlers.start import start_state
from app.middlewares.locales import LocaleMiddleware
from app.middlewares.spam import AntiSpamMiddleware
from databases import Database


def install_bot():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TELEGRAM_API_TOKEN)
    dp = Dispatcher(bot)
    database = Database(DB_URL)
    main_state = AiogramMainRouter(dp)

    dp.middleware.setup(LocaleMiddleware("./localization"))
    dp.middleware.setup(AntiSpamMiddleware(limit=30, delay=30))

    main_state.container.bind_constant(Database, database)
    main_state.container.bind(SettingsRepository, SettingsRepository)
    main_state.container.bind(UserRepository, UserRepository)
    main_state.container.bind(BusStopRepository, BusStopRepository)
    main_state.container.bind(BusStopService, BusStopService)

    main_state.include_router(start_state)
    main_state.include_router(other_state)
    main_state.include_router(settings_state)

    main_state.install(default_state_name="start", storage=MemoryStorage())

    return dp, database


if __name__ == "__main__":
    dp, database = install_bot()
    executor.start_polling(dp, skip_updates=True, on_startup=startup_wrapper(database), on_shutdown=shutdown_wrapper(database))
