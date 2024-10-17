from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.handlers.users.start import ru_language, bot_start
from tgbot.keyboards.inline.catalog import flat
from tgbot.states.users import Flat_rent


async def get_rent_category(message: types.Message):
    db = message.bot.get("db")
    _ = message.bot.get("lang")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main = _("Главное Меню")
    back = _("Назад")
    # main = "Главное Меню"
    # back = "Назад"
    markup.insert(KeyboardButton(text=main))
    markup.insert(KeyboardButton(text=back))

    sub1categories = []
    uz_sub1categories = []

    if await ru_language(message):
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_category(
                category="Аренда"):
            if sub1category not in sub1categories:
                sub1categories.append(sub1category)
                markup.add(KeyboardButton(text=sub1category))
    else:
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_category(
                category="Аренда"):
            if sub1category_uz not in uz_sub1categories:
                uz_sub1categories.append(sub1category_uz)
                markup.add(KeyboardButton(text=sub1category_uz))
    send_text = _("Выберите район")
    await message.answer(send_text, reply_markup=markup)
    await Flat_rent.Sub1.set()


# Flat_rent.Sub1
async def get_rent_sub1category(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main = _("Главное Меню")
    back = _("Назад")
    # main = "Главное Меню"
    # back = "Назад"
    send_text = _("Выберите количество комнат")

    markup.insert(KeyboardButton(text=main))
    markup.insert(KeyboardButton(text=back))
    if message.text == back:
        await state.reset_state()
        await bot_start(message, state)
    else:
        sub2categories = []
        uz_sub2categories = []

        if await ru_language(message):
            try:
                select = await db.select_flat(sub1category=message.text)
                code = select.get("sub1_code")
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub1category(
                        category="Аренда", sub1category=message.text)):
                    if sub2category not in sub2categories:
                        sub2categories.append(sub2category)
                for room in sorted(sub2categories):
                    markup.add(KeyboardButton(text=room))
                await message.answer(send_text, reply_markup=markup)
                await state.update_data(area=code)
                await Flat_rent.Sub2.set()
            except:
                # await state.reset_state()
                # await get_sale_category(message)
                pass
        else:
            try:
                select = await db.select_flat(sub1category_uz=message.text)
                code = select.get("sub1_code")
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub1category_uz(
                        category="Аренда", sub1category_uz=message.text)):
                    if sub2category_uz not in uz_sub2categories:
                        uz_sub2categories.append(sub2category_uz)
                for room in sorted(sub2categories):
                    markup.add(KeyboardButton(text=room))
                await message.answer(send_text, reply_markup=markup)
                await state.update_data(area=code)
                await Flat_rent.Sub2.set()
            except:
                # await state.reset_state()
                # await get_sale_category(message)
                pass


# Flat_rent.Sub2
async def get_rent_sub2category(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    data = await state.get_data()
    area = data.get("area")

    back = _("Назад")
    order = _("Заказать осмотр квартиры")
    main = _("Главное Меню")
    send_text = _("Все квартиры: ")

    if message.text == back:
        await state.reset_state()
        await get_rent_category(message)
    else:
        if await ru_language(message):
            try:
                select = await db.select_flat(sub1_code=area)
                select.get("article_url")
                sub1cat = select.get("sub1category")
                await state.reset_state()
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub2category(
                        category="Аренда", sub1category=sub1cat, sub2category=message.text)):
                    inline_markup = InlineKeyboardMarkup(row_width=2)
                    inline_markup.insert(InlineKeyboardButton(text=f"👍 ({like})",
                                                              callback_data=flat.new(action="like", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=f"👎 ({dislike})",
                                                              callback_data=flat.new(action="dislike", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=order,
                                                              callback_data=flat.new(action="view", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=back,
                                                              callback_data=flat.new(action="back", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    await message.answer(article_url, reply_markup=inline_markup)
                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                markup.insert(KeyboardButton(text=main))
                await message.answer(send_text, reply_markup=markup)
            except:
                pass
        else:
            try:
                select = await db.select_flat(sub1_code=area)
                select.get("article_url")
                sub1cat_uz = select.get("sub1category_uz")
                await state.reset_state()
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub2category_uz(
                        category="Аренда", sub1category_uz=sub1cat_uz, sub2category_uz=message.text)):
                    inline_markup = InlineKeyboardMarkup(row_width=2)
                    inline_markup.insert(InlineKeyboardButton(text=f"👍 ({like})",
                                                              callback_data=flat.new(action="like", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=f"👎 ({dislike})",
                                                              callback_data=flat.new(action="dislike", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=order,
                                                              callback_data=flat.new(action="view", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=back,
                                                              callback_data=flat.new(action="back", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Аренда", sub1=area)))
                    await message.answer(article_url_uz, reply_markup=inline_markup)
                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                markup.insert(KeyboardButton(text=main))
                await message.answer(send_text, reply_markup=markup)
            except:
                pass


async def back_sub1(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    await call.answer()
    categ = callback_data.get("categ")
    sub1 = callback_data.get("sub1")
    await call.answer()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main = _("Главное Меню")
    back = _("Назад")
    # main = "Главное Меню"
    # back = "Назад"
    markup.insert(KeyboardButton(text=main))
    markup.insert(KeyboardButton(text=back))

    sub2categories = []
    uz_sub2categories = []

    if await ru_language(call):
        select = await db.select_flat(sub1_code=int(sub1))
        select.get("sub2category")
        sub1cat = select.get("sub1category")
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(
                await db.select_in_sub1category(
                    category=categ, sub1category=sub1cat)):
            if sub2category not in sub2categories:
                sub2categories.append(sub2category)
        for room in sorted(sub2categories):
            markup.add(KeyboardButton(text=room))

    else:
        select = await db.select_flat(sub1_code=int(sub1))
        select.get("sub2category_uz")
        sub1cat_uz = select.get("sub1category_uz")
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(
                await db.select_in_sub1category_uz(
                    category=categ, sub1category_uz=sub1cat_uz)):
            if sub2category_uz not in uz_sub2categories:
                uz_sub2categories.append(sub2category_uz)
        for room in sorted(sub2categories):
            markup.add(KeyboardButton(text=room))
    send_text = _("Выберите количество комнат")
    await call.message.answer(send_text, reply_markup=markup)
    await Flat_rent.Sub2.set()
    await state.update_data(categ=categ)
    await state.update_data(area=sub1)


def register_rent(dp: Dispatcher):
    dp.register_message_handler(get_rent_category, text=["Аренда", "Ijara"])
    dp.register_message_handler(get_rent_sub1category, state=Flat_rent.Sub1)
    dp.register_message_handler(get_rent_sub2category, state=Flat_rent.Sub2)
    dp.register_callback_query_handler(back_sub1, flat.filter(action="back", categ="Аренда"))


