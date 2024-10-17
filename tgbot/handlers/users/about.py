from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.users.start import admins_list, ru_language
from tgbot.keyboards.default.main_menu import admin_menu, m_menu, admin_menu_uz, m_menu_uz
from tgbot.keyboards.inline.catalog import flat
from tgbot.states.users import Custom


async def about_us(message: types.Message):
    _ = message.bot.get("lang")
    text = _("Агентство недвижимости\n"
             "<b>Поможет</b>\n"
             "☑️ продать/купить\n"
             "☑️ снять/сдать\n"
             "☑️ оформить наследство\n"
             "☑️ бесплатная консультация\n"
             "\n"
             "<b>+998 99 036-44-44</b>")
    if await ru_language(message):
        await message.bot.send_photo(message.chat.id, photo="AgACAgIAAxkBAAIiT2Op3-hkfQmUnsPfrPydQXjL6P14AALVxjEb7s9RSWlZ3ZP0cJsvAQADAgADeQADLAQ", caption=text)
    else:
        await message.bot.send_photo(message.chat.id, photo="AgACAgIAAxkBAAIiT2Op3-hkfQmUnsPfrPydQXjL6P14AALVxjEb7s9RSWlZ3ZP0cJsvAQADAgADeQADLAQ", caption=text)


async def custom(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    send_text = _("Выберите язык")
    main = _("Главное Меню")
    print(_)
    lang_custom = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    lang_custom.insert(KeyboardButton(text="🇷🇺 Ru"))
    lang_custom.insert(KeyboardButton(text="🇺🇿 Uz"))
    lang_custom.insert(KeyboardButton(text=main))
    await message.answer(send_text, reply_markup=lang_custom)
    await Custom.Lang.set()


# Custom.Lang
async def custom_lang(message: types.Message, state: FSMContext):
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
    await db.update_user(telegram_id=message.from_user.id, language=language)


async def Etwas(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await message.answer("start")
    for i in range(125, 536):
        try:
            await db.add_user(
                first_name=message.from_user.first_name,
                username=message.from_user.username,
                telegram_id=int(f"{message.from_user.id}{i}"),
                language="ru"
            )
        except:
            pass
    await message.answer("done")


def register_adout(dp: Dispatcher):
    dp.register_message_handler(about_us, text=["ℹ️ О Нас", "ℹ️ Biz haqimizda"])
    dp.register_message_handler(about_us, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(custom, text=["⚙️ Sozlamalar", "⚙️ Настройки"])
    dp.register_message_handler(custom_lang, state=Custom.Lang, text=["🇷🇺 Ru", "🇺🇿 Uz"])
    dp.register_message_handler(Etwas, Command("etwas"))



