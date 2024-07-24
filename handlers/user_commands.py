from data.database import request
from keyboards import reply, inline

from aiogram import Router, Bot, html
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        await message.answer(f"Здравствуйте, {html.bold(message.from_user.first_name)}, что вас интересует?", reply_markup=inline.main_keyboard())
        await BotDB.create_user(message.from_user.id, message.from_user.username)
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()