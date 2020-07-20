import asyncio

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit: int, delay: int = 60) -> None:
        super().__init__()
        self._limit = limit
        self._delay = delay
        self.users_requests = {}
        self.is_running = False

    async def check_user(self, user_obj: types.User) -> bool:
        if not self.is_running:
            asyncio.create_task(self._run_cleaner())

        number_of_user_requests = self.users_requests.get(user_obj.id)
        if number_of_user_requests is None:
            self.users_requests[user_obj.id] = 1
        elif number_of_user_requests >= self._limit:
            return True
        else:
            self.users_requests[user_obj.id] = number_of_user_requests + 1
        return False

    async def _run_cleaner(self) -> None:
        while self.is_running:
            self.users_requests.clear()
            await asyncio.sleep(self._delay)

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        spam_state = await self.check_user(message.from_user)
        if spam_state:
            await message.answer(data["locale"].spam_limit)
            raise CancelHandler()

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict) -> None:
        spam_state = await self.check_user(query.from_user)
        if spam_state:
            await query.answer(data["locale"].spam_limit)
            raise CancelHandler()
