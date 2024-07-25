from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from data.database import request
from keyboards.inline import create_form

router = Router()


@router.callback_query(F.data == 'my_form')
async def my_user_form(callback: CallbackQuery):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = callback.message.chat.id
        if await BotDB.get_user_form(member_id):
            member_form = await BotDB.user_form_list(member_id)

            await callback.message.answer_photo(
                member_form[6],
                f'Имя: {member_form[2]}\nВозраст: {member_form[3]}\nПол: {member_form[4]}\nО себе: {member_form[5]}',
                reply_markup=create_form()
            )
        else:
            await callback.message.answer("Упс... вашей анкеты нету!!!", reply_markup=create_form())
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()