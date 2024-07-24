from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class AdminMode:
    def __init__(self):
        self.ids = ['1069370364', '111']

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        member_id = str(event.from_user.id)
        if member_id in self.ids:
            return await handler(event, data)
        await event.answer(f'Сорян... Сейчас мной могут пользоваться, только персонал!!!')