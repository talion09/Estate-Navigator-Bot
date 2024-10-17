from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.users.start import bot_start
from tgbot.keyboards.default.cancel import cancel
from tgbot.states.users import Admin


async def custom_adm(message):
    db = message.bot.get("db")
    admins_1 = []
    admins_2 = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Главное Меню"))
    for id, telegram_id, name, level in await db.select_all_admins():
        if level ==1:
            admins_1.append(telegram_id)
        if level == 2:
            admins_2.append(telegram_id)
    if message.from_user.id in admins_1:
        markup.insert(KeyboardButton(text="Админы"))
        markup.insert(KeyboardButton(text="Квартиры"))
    else:
        markup.insert(KeyboardButton(text="Квартиры"))
    return markup


async def admin(message: types.Message):
    markup = await custom_adm(message)
    await message.answer("Что вы хотите сделать ?", reply_markup=markup)


async def cancel_admin(message: types.Message, state: FSMContext):
    await state.reset_state()
    await admin(message)


def register_custom_admins(dp: Dispatcher):
    dp.register_message_handler(admin, IsAdmin(), text="Администрация")