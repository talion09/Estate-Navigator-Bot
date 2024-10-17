from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Продажа"),
            KeyboardButton(text="Аренда")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="⚙️ Настройки")
        ],
        [
            KeyboardButton(text="Администрация"),
        ]
    ], resize_keyboard=True)

admin_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Sotiladi"),
            KeyboardButton(text="Ijara")
        ],
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ],
        [
            KeyboardButton(text="Администрация"),
        ]
    ], resize_keyboard=True)


m_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Продажа"),
            KeyboardButton(text="Аренда")
        ],
        [
            KeyboardButton(text="ℹ️ О Нас"),
            KeyboardButton(text="⚙️ Настройки")
        ]
    ], resize_keyboard=True)


m_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Sotiladi"),
            KeyboardButton(text="Ijara")
        ],
        [
            KeyboardButton(text="ℹ️ Biz haqimizda"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ]
    ], resize_keyboard=True)