from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


flat_customize_adm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Квартиру"),
            KeyboardButton(text="Удалить Квартиру"),
        ],
        [
            KeyboardButton(text="Редактировать Квартиру"),
            KeyboardButton(text="Главное Меню")
        ]
    ],
    resize_keyboard=True
)


flat_customize = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Квартиру"),
            KeyboardButton(text="Редактировать Квартиру")

        ],
        [
            KeyboardButton(text="Главное Меню")
        ]
    ],
    resize_keyboard=True
)