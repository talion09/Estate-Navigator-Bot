from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отменить")
        ]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)


phone_custom = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Поделиться контактом",
                           request_contact=True)
        ],
        [
            KeyboardButton(text="Отменить")
        ]
    ],
    resize_keyboard=True
)

lang_custom = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇷🇺 Ru"),
            KeyboardButton(text="🇺🇿 Uz")
        ],
        [
            KeyboardButton(text="Отменить")
        ]
    ],
    resize_keyboard=True
)

