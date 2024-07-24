from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def main_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Моя Анкета", callback_data='create'),
                InlineKeyboardButton(text='Поиск Анкет', callback_data='search')
            ]
        ]
    )
    return main