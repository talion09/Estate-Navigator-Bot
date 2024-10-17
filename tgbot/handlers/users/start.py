from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.config import load_config
from tgbot.keyboards.default.language import lang
from tgbot.keyboards.default.main_menu import m_menu, admin_menu, admin_menu_uz, m_menu_uz
from tgbot.states.users import User, Admin, Flat, Flat_rent, Add_Flat, Custom, Edit_flat, Del_Flat


async def canc(message):
    cancel = ReplyKeyboardMarkup(resize_keyboard=True)
    if await ru_language(message):
        cancel.add(KeyboardButton(text="Отменить"))
    else:
        cancel.add(KeyboardButton(text="Bekor qilish"))
    return cancel


async def ru_language(message):
    db = message.bot.get("db")
    user_in_db = await db.select_user(telegram_id=int(message.from_user.id))
    if user_in_db.get("language") == "ru":
        return True


async def admins_list(message):
    db = message.bot.get("db")
    admins_list = []
    for id, telegram_id, name, level in await db.select_all_admins():
        admins_list.append(telegram_id)
    if message.from_user.id in admins_list:
        if await ru_language(message):
            menu = admin_menu
        else:
            menu = admin_menu_uz
    else:
        if await ru_language(message):
            menu = m_menu
        else:
            menu = m_menu_uz
    return menu


async def bot_start(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await state.reset_state()
    try:
        user_in_db = await db.select_user(telegram_id=int(message.from_user.id))
        username = user_in_db.get("username")
        full_name = user_in_db.get("first_name")
        menu = await admins_list(message)
        if username != message.from_user.username:
            await db.update_user(telegram_id=int(message.from_user.id), username=message.from_user.username)
        if user_in_db.get("language") == "ru":
            await message.answer(f"<b>{full_name}</b>, выберите что вас интересует:", reply_markup=menu)
        else:
            await message.answer(f"<b>{full_name}</b>, Sizni qiziqtirgan narsani tanlang:", reply_markup=menu)
    except AttributeError:
        await message.answer(
            f"Здравствуйте! {message.from_user.full_name}\nВыберите язык:\n\nAssalomu alaykum!\nTilni tanlang:",
            reply_markup=lang)
        await User.Lang.set()


# User.Lang
async def info_lang(message: types.Message, state: FSMContext):
    name_user = message.from_user.full_name
    db = message.bot.get("db")
    admins_list = []
    for id, telegram_id, name, level in await db.select_all_admins():
        admins_list.append(telegram_id)
    language = str()
    await state.reset_state()
    if message.text == "🇷🇺 Ru":
        language = "ru"
        if message.from_user.id in admins_list:
            menu = admin_menu
        else:
            menu = m_menu
        await message.answer(
            f"{name_user}, Выберите что вас интересует:",
            reply_markup=menu)
    elif message.text == "🇺🇿 Uz":
        language = "uz"
        if message.from_user.id in admins_list:
            menu = admin_menu_uz
        else:
            menu = m_menu_uz
        await message.answer(
            f"{name_user}, Sizni qiziqtirgan narsani tanlang:",
            reply_markup=menu)
    await db.add_user(
        first_name=message.from_user.first_name,
        username=message.from_user.username,
        telegram_id=message.from_user.id,
        language=language
    )


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state="*")
    dp.register_message_handler(bot_start, text=["Главное Меню", "Asosiy menyu"])
    dp.register_message_handler(bot_start, text=["Главное Меню", "Asosiy menyu"], state=[Flat.Sub1, Flat.Sub2,
                                                                                         Flat_rent.Sub1, Flat_rent.Sub2,
                                                                                         Flat.Urls, Flat_rent.Urls,
                                                                                         User.Phone, Add_Flat.Categ, Custom.Lang,
                                                                                         Edit_flat.Categ, Del_Flat.Categ])
    dp.register_message_handler(info_lang, state=User.Lang, text=["🇷🇺 Ru", "🇺🇿 Uz"])
