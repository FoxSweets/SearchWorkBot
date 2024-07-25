import asyncio
import logging
import sys
from config_reader import config

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import user_commands, text_commands
from callback import create_form, user_form
from middleware.admin_mode import AdminMode

from data.database import create, request


async def main():
    await create.create_database()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(config.bot_token.get_secret_value(), default=default)

    if len(sys.argv) == 2:
        if sys.argv[1] == 'admin' or sys.argv[1] == '1':
            dp.message.middleware(AdminMode())

    dp.include_routers(
        user_form.router,
        create_form.router,
        user_commands.router,
        text_commands.router
    )

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())