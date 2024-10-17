from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, ReplyKeyboardRemove

from tgbot.filters.is_admin import IsAdmin, IsAdmin_1
from tgbot.handlers.users.start import bot_start, admins_list
from tgbot.keyboards.default.cancel import cancel, back
from tgbot.keyboards.default.confirm import confirm
from tgbot.keyboards.inline.catalog import flat, delete_id
from tgbot.states.users import Admin, Add_Flat, Add_Room, Del_Flat


async def delete_flat(message: types.Message):
    db = message.bot.get("db")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Продажа"))
    markup.insert(KeyboardButton(text="Аренда"))
    markup.insert(KeyboardButton(text="Главное Меню"))
    await message.answer("Выберите категорию:", reply_markup=markup)
    await Del_Flat.Categ.set()


async def areas_rent(message, state, categ):
    db = message.bot.get("db")
    sub1categories = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Назад"))
    for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_category(
            category=categ):
        if sub1category not in sub1categories:
            sub1categories.append(sub1category)
            markup.insert(KeyboardButton(text=sub1category))
    await state.update_data(categ=categ)
    await message.answer(f"Выберите район ", reply_markup=markup)
    await Del_Flat.Sub1.set()


async def rooms_rent(message, state, categ, sub1categ):
    db = message.bot.get("db")
    if message.text == "Назад":
        await state.reset_state()
        await delete_flat(message)
    else:
        try:
            select = await db.select_flat(sub1category=sub1categ, category=categ)
            select.get("sub2category")
            sub2categories = []
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Назад"))
            for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_sub1category(
                    category=categ, sub1category=sub1categ):
                if sub2category not in sub2categories:
                    sub2categories.append(sub2category)
            for room in sorted(sub2categories):
                markup.insert(KeyboardButton(text=room))
            await message.answer(f"Выберите количество комнат", reply_markup=markup)
            await state.update_data(sub1=sub1categ)
            await Del_Flat.Sub2.set()
        except:
            pass


# Del_Flat.Categ
async def select_in_categ(message: types.Message, state: FSMContext):
    await areas_rent(message, state, message.text)


# Del_Flat.Sub1
async def select_in_sub1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    categ = data.get("categ")
    if message.text == "Назад":
        await state.reset_state()
        await delete_flat(message)
    else:
        await rooms_rent(message, state, categ, message.text)


# Del_Flat.Sub2
async def select_in_sub2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    sub1 = data.get("sub1")
    if message.text == "Назад":
        await areas_rent(message, state, categ)
    else:
        try:
            select = await db.select_flat(sub2category=message.text)
            select.get("article_url")
            await state.reset_state()
            await message.answer("Все квартиры:", reply_markup=ReplyKeyboardRemove())
            for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(
                    await db.select_in_sub2category(
                        category=categ, sub1category=sub1, sub2category=message.text)):
                inline_markup = InlineKeyboardMarkup(row_width=3)
                inline_markup.insert(InlineKeyboardButton(text=f"Удалить",
                                                          callback_data=delete_id.new(id=id, action="delete",
                                                                                      categ=categ)))
                inline_markup.insert(InlineKeyboardButton(text=f"Назад",
                                                          callback_data=delete_id.new(id=id, action="back",
                                                                                      categ=categ)))
                await message.answer(article_url, reply_markup=inline_markup)
        except:
            pass


async def delete_id_flat(call: CallbackQuery, callback_data: dict):
    db = call.message.bot.get("db")
    id = callback_data.get("id")
    await call.answer()
    await db.delete_flat(id=int(id))
    menu = await admins_list(call)
    await call.message.answer("Квартира была удалена!", reply_markup=menu)


async def back_from_del(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = call.message.bot.get("db")
    id = callback_data.get("id")
    await call.answer()

    select = await db.select_flat(id=int(id))
    categ = select.get("category")
    sub1 = select.get("sub1category")
    sub2categories = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Назад"))
    for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_sub1category(
            category=categ, sub1category=sub1):
        if sub2category not in sub2categories:
            sub2categories.append(sub2category)
    for room in sorted(sub2categories):
        markup.insert(KeyboardButton(text=room))
    await call.message.answer(f"Выберите количество комнат", reply_markup=markup)
    await state.update_data(sub1=sub1)
    await state.update_data(categ=categ)
    await Del_Flat.Sub2.set()


def register_delete_flat(dp: Dispatcher):
    dp.register_message_handler(delete_flat, IsAdmin_1(), text="Удалить Квартиру")
    dp.register_message_handler(select_in_categ, IsAdmin_1(), state=Del_Flat.Categ, text=["Продажа", "Аренда"])
    dp.register_message_handler(select_in_sub1, state=Del_Flat.Sub1)
    dp.register_message_handler(select_in_sub2, state=Del_Flat.Sub2)
    dp.register_callback_query_handler(delete_id_flat, delete_id.filter(action="delete"), IsAdmin_1())
    dp.register_callback_query_handler(back_from_del, delete_id.filter(action="back"),  IsAdmin_1())

