from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Верно"),
            KeyboardButton(text="Отменить")

        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)