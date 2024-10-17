from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.handlers.users.start import ru_language, bot_start
from tgbot.keyboards.inline.catalog import flat
from tgbot.states.users import Flat_rent


async def education(message: types.Message):
    db = message.bot.get("db")
    _ = message.bot.get("lang")

    await message.answer("VIDEO")


async def cart(message: types.Message):
    db = message.bot.get("db")
    _ = message.bot.get("lang")


def register_education(dp: Dispatcher):
    dp.register_message_handler(education, text=["Обучение", "Ta'lim"])
    dp.register_message_handler(cart, text=["🗑 Корзина", "🗑 Savatcha"])


