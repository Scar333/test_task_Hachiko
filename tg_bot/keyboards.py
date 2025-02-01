from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает простые кнопки"""

    buttons = ['Проверить IMEI']

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons[0])]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
