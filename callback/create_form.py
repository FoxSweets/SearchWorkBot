from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from data.database import request
from utils.states import Form
from keyboards.builders import profile
from keyboards.reply import rmk

router = Router()


@router.callback_query()
async def profile_rooms_user(callback: CallbackQuery, state: FSMContext):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        callback_data = callback.data
        if callback_data == "create":
            await callback.message.answer("Хорошо, давайте создадим вашу анкету, я просто задам несколько вопросов")
            await state.set_state(Form.name)
            await callback.message.answer("Введите своё имя", reply_markup=profile(callback.message.chat.first_name))
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer('Теперь укажите сколько вам лет!!', reply_markup=rmk)


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
    await state.update_data(sex=message.text)
    await state.set_state(Form.about)
    await message.answer('Расскажите о себе!', reply_markup=rmk)


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
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()

    formatted_text = []
    [
        formatted_text.append(f"{key}: {value}")
        for key, value in data.items()
    ]

    await message.answer_photo(
        photo_file_id,
        '\n'.join(formatted_text)
    )


@router.message(Form.photo)
async def incorrect_form_photo(message: Message):
    await message.answer('Отправьте фото!')