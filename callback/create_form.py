from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from data.database import request
from utils.states import Form

from keyboards.builders import profile
from keyboards.reply import rmk
from keyboards.inline import create_form

router = Router()


@router.callback_query(F.data == 'create_form')
async def create_form_user(callback: CallbackQuery, state: FSMContext):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = callback.message.chat.id
        await callback.message.answer("Хорошо, давайте создадим вашу анкету, я просто задам несколько вопросов")
        await state.set_state(Form.name)
        member_name = await BotDB.user_form_name(member_id=member_id)
        name_list = [callback.message.chat.first_name]
        if member_name != 'None':
            name_list = [callback.message.chat.first_name, member_name]
        await callback.message.answer("Введите своё имя", reply_markup=profile(name_list))
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = message.from_user.id
        await state.update_data(name=message.text)
        await state.set_state(Form.age)
        member_age = await BotDB.user_form_age(member_id=member_id)
        age_list = rmk
        if member_age != 'None':
            age_list = profile(str(member_age))
        await message.answer('Теперь укажите сколько вам лет!!', reply_markup=age_list)
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.message(Form.age)
async def form_age(message: Message, state: FSMContext):
    if (message.text.isdigit()) and (len(message.text) <= 2) and (int(message.text) > 0):
        await state.update_data(age=message.text)
        await state.set_state(Form.sex)
        await message.answer("Укажите свой пол", reply_markup=profile(['Парень', 'Девушка']))
    else:
        await message.answer('Введите число, ещё раз!')


@router.message(Form.sex, F.text.casefold().in_(['парень', 'девушка']))
async def form_sex(message: Message, state: FSMContext):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = message.from_user.id
        await state.update_data(sex=message.text)
        await state.set_state(Form.about)
        member_about = await BotDB.user_form_about(member_id=member_id)
        about_list = rmk
        if member_about != 'None':
            about_list = profile(str(member_about))
        await message.answer('Расскажите о себе!', reply_markup=about_list)
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.message(Form.sex)
async def incorrect_form_sex(message: Message):
    await message.answer('Такого пола нету, нажмите на кнопку снизу')


@router.message(Form.about)
async def form_about(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer('Расскажите что-то больше')
    else:
        await state.update_data(about=message.text)
        await state.set_state(Form.photo)
        await message.answer('Скиньте фото!')


@router.message(Form.photo, F.photo)
async def form_photo(message: Message, state: FSMContext):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = message.from_user.id
        photo_file_id = message.photo[-1].file_id
        data = await state.get_data()
        await state.clear()

        formatted_text = {}
        for key, value in data.items():
            formatted_text[key] = value

        print(formatted_text)
        await BotDB.update_user_form(member_id, formatted_text['name'], formatted_text['age'], formatted_text['sex'], formatted_text['about'], photo_file_id)

        await message.answer_photo(
            photo_file_id,
            f'Имя: {formatted_text['name']}\nВозраст: {formatted_text['age']}\nПол: {formatted_text['sex']}\nО себе: {formatted_text['about']}',
            reply_markup=create_form()
        )
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.message(Form.photo)
async def incorrect_form_photo(message: Message):
    await message.answer('Отправьте фото!')