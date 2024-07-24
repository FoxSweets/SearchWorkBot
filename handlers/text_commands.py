from data.database import request

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
router = Router()


@router.message()
async def echo(message: Message, bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        pass
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()