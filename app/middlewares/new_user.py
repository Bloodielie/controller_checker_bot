from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models.settings import Settings
from app.models.user import Users


class NewUserMiddleware(BaseMiddleware):
    async def setup_user(self, data: dict, user_obj: types.User) -> None:
        user_id = user_obj.id

        user = await Users.get_or_none(telegram_id=user_id).prefetch_related("settings")
        if user is None:
            user = await Users.create(
                telegram_id=user_id, username=(user_obj.username or "NONE"), settings=await Settings.create(),
            )

        data["user"] = user

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        await self.setup_user(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict) -> None:
        await self.setup_user(data, query.from_user)
