from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def main_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Моя Анкета", callback_data='my_form'),
                InlineKeyboardButton(text='Искать Анкеты', callback_data='search_form')
            ]
        ]
    )
    return main


def create_form():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Создать анкету", callback_data='create_form'),
                InlineKeyboardButton(text='Искать анкеты', callback_data='search_form')
            ]
        ]
    )
    return main


def accept_create_form():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✔", callback_data='accept_form'),
                InlineKeyboardButton(text='❌', callback_data='create_form')
            ]
        ]
    )
    return main