from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from data.database import request

from keyboards.reply import rmk
from keyboards.inline import choice_search_form

from random import choice

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
        profiles = await BotDB.get_profiles(member_id, 'Соискатель')
        rng_profile = choice(profiles)

        member_form = await BotDB.user_form_list(rng_profile)

        await callback.message.answer_photo(
            member_form[9],
            f'Имя: {member_form[3]}\nВозраст: {member_form[4]}\nПол: {member_form[5]}\nМесто проживания: {member_form[6]} | г.{member_form[7]}\n\nО себе: {member_form[8]}',
        )

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
        await callback.message.answer("ПОКА НЕТУ")
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()