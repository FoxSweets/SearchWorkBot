from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from data.database import request

from keyboards.reply import rmk
from keyboards.inline import choice_search_form

router = Router()


@router.callback_query(F.data == 'search_form')
async def _search_form(callback: CallbackQuery):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = callback.message.chat.id
        await callback.message.answer("Хорошо, выберите кого вы хотите искать!", reply_markup=choice_search_form())
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.callback_query(F.data == 'search_worker')
async def _search_worker(callback: CallbackQuery):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = callback.message.chat.id
        await callback.message.answer("Хорошо, ищём работника...")
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.callback_query(F.data == 'search_company')
async def _search_company(callback: CallbackQuery):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = callback.message.chat.id
        await callback.message.answer("Хорошо, ищём компанию...")
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()