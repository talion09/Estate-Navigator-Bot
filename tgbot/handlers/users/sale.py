from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

from tgbot.handlers.users.start import ru_language, bot_start, admins_list
from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.inline.catalog import flat
from tgbot.states.users import User, Flat


async def get_sale_category(message: types.Message):
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
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_category(
                category="Продажа")):
            if sub1category not in sub1categories:
                sub1categories.append(sub1category)
                markup.add(KeyboardButton(text=sub1category))
    else:
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_category(
                category="Продажа")):
            if sub1category_uz not in uz_sub1categories:
                uz_sub1categories.append(sub1category_uz)
                markup.add(KeyboardButton(text=sub1category_uz))
    # send_text = _("Выберите район")
    await message.answer(f"Выберите район", reply_markup=markup)
    await Flat.Sub1.set()


# Flat.Sub1
async def get_sale_sub1category(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main = _("Главное Меню")
    back = _("Назад")
    # main = "Главное Меню"
    # back = "Назад"
    markup.insert(KeyboardButton(text=main))
    markup.insert(KeyboardButton(text=back))
    if message.text == back:
        await state.reset_state()
        await bot_start(message, state)
    else:
        sub2categories = []
        uz_sub2categories = []
        send_text = _("Выберите количество комнат")

        if await ru_language(message):
            try:
                select = await db.select_flat(sub1category=message.text)
                code = select.get("sub1_code")
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub1category(
                        category="Продажа", sub1category=message.text)):
                    if sub2category not in sub2categories:
                        sub2categories.append(sub2category)
                for room in sorted(sub2categories):
                    markup.add(KeyboardButton(text=room))
                await message.answer(send_text, reply_markup=markup)
                await state.update_data(area=code)
                await Flat.Sub2.set()
            except:
                # await state.reset_state()
                # await get_sale_category(message)
                pass
        else:
            try:
                select = await db.select_flat(sub1category_uz=message.text)
                code = select.get("sub1_code")
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub1category_uz(
                        category="Продажа", sub1category_uz=message.text)):
                    if sub2category_uz not in uz_sub2categories:
                        uz_sub2categories.append(sub2category_uz)
                for room in sorted(uz_sub2categories):
                    markup.add(KeyboardButton(text=room))
                await message.answer(send_text, reply_markup=markup)
                await state.update_data(area=code)
                await Flat.Sub2.set()
            except:
                # await state.reset_state()
                # await get_sale_category(message)
                pass


# Flat.Sub2
async def get_sale_sub2category(message: types.Message, state: FSMContext):
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
        await get_sale_category(message)
    else:
        if await ru_language(message):
            try:
                select = await db.select_flat(sub1_code=area)
                select.get("article_url")
                sub1cat = select.get("sub1category")
                await state.reset_state()
                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub2category(
                        category="Продажа", sub1category=sub1cat, sub2category=message.text)):
                    inline_markup = InlineKeyboardMarkup(row_width=2)
                    inline_markup.insert(InlineKeyboardButton(text=f"👍 ({like})",
                                                              callback_data=flat.new(action="like", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=f"👎 ({dislike})",
                                                              callback_data=flat.new(action="dislike", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=order,
                                                              callback_data=flat.new(action="view", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=back,
                                                              callback_data=flat.new(action="back", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    await message.answer(article_url, reply_markup=inline_markup)
                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                markup.insert(KeyboardButton(text=main))
                await message.answer(send_text, reply_markup=markup)
            except:
                # await state.reset_state()
                # await get_sale_category(message)
                pass
        else:
            try:
                select = await db.select_flat(sub1_code=area)
                select.get("article_url_uz")
                sub1cat_uz = select.get("sub1category_uz")
                await state.reset_state()

                for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in sorted(await db.select_in_sub2category_uz(
                        category="Продажа", sub1category_uz=sub1cat_uz, sub2category_uz=message.text)):
                    inline_markup = InlineKeyboardMarkup(row_width=2)
                    inline_markup.insert(InlineKeyboardButton(text=f"👍 ({like})",
                                                              callback_data=flat.new(action="like", id=id,
                                                                                     likes=like, dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=f"👎 ({dislike})",
                                                              callback_data=flat.new(action="dislike", id=id,
                                                                                     likes=like, dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=order,
                                                              callback_data=flat.new(action="view", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    inline_markup.insert(InlineKeyboardButton(text=back,
                                                              callback_data=flat.new(action="back", id=id,
                                                                                     likes=like,
                                                                                     dislikes=dislike,
                                                                                     views=viewed, categ="Продажа", sub1=area)))
                    await message.answer(article_url_uz, reply_markup=inline_markup)
                markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                markup.insert(KeyboardButton(text=main))
                await message.answer(send_text, reply_markup=markup)
            except:
                # await state.reset_state()
                # await get_sale_category(message)
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
    await Flat.Sub2.set()
    await state.update_data(categ=categ)
    await state.update_data(area=sub1)


async def likes_dislikes(call, id, likes, dislikes, views, categ, area):
    db = call.message.bot.get("db")
    _ = call.bot.get("lang")
    flats = await db.select_flat(id=int(id))
    if await ru_language(call):
        url = flats.get("article_url")
    else:
        url = flats.get("article_url_uz")
    back = _("Назад")
    # back = "Назад"
    order = _("Заказать осмотр квартиры")
    # order = "Заказать осмотр квартиры"

    inline_markup = InlineKeyboardMarkup(row_width=2)
    inline_markup.insert(InlineKeyboardButton(text=f"👍 ({likes})",
                                              callback_data=flat.new(action="like", id=id, likes=likes,
                                                                     dislikes=dislikes, views=views,
                                                                     categ=categ, sub1=area)))
    inline_markup.insert(InlineKeyboardButton(text=f"👎 ({dislikes})",
                                              callback_data=flat.new(action="dislike", id=id, likes=likes,
                                                                     dislikes=dislikes, views=views,
                                                                     categ=categ, sub1=area)))
    inline_markup.insert(InlineKeyboardButton(text=order,
                                              callback_data=flat.new(action="view", id=id,
                                                                     likes=likes,
                                                                     dislikes=dislikes,
                                                                     views=views,
                                                                     categ=categ, sub1=area)))
    inline_markup.insert(InlineKeyboardButton(text=back,
                                              callback_data=flat.new(action="back", id=id,
                                                                     likes=likes,
                                                                     dislikes=dislikes,
                                                                     views=views,
                                                                     categ=categ, sub1=area)))
    try:
        await call.bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=url,
                                         reply_markup=inline_markup)
    except:
        pass


async def more_likes(call: CallbackQuery, callback_data: dict):
    db = call.message.bot.get("db")
    id = callback_data.get("id")
    likes = int(callback_data.get("likes"))
    dislikes = int(callback_data.get("dislikes"))
    views = int(callback_data.get("views"))
    categ = callback_data.get("categ")
    sub1 = callback_data.get("sub1")
    await call.answer()

    user = await db.select_user(telegram_id=int(call.from_user.id))
    disliked_ids = user.get("disliked_id")
    liked_ids = user.get("liked_id")
    if disliked_ids is not None:
        disflat_ids = disliked_ids.split(",")
        if str(id) in disflat_ids:
            disflat_ids.remove(str(id))
            dislikes -= 1
            if len(disflat_ids) == 0:
                await db.update_user(telegram_id=int(call.from_user.id), disliked_id=None)
            else:
                disflat = ",".join(disflat_ids)
                await db.update_user(telegram_id=int(call.from_user.id), disliked_id=str(disflat))
            await db.update_flat(id=int(id), dislikes=int(dislikes))
        else:
            pass
    else:
        pass
    if liked_ids is not None:
        flat_ids = liked_ids.split(",")
        if str(id) not in flat_ids:
            flat_ids.append(str(id))
            liked_flats = ",".join(flat_ids)
            likes += 1
            await db.update_user(telegram_id=int(call.from_user.id), liked_id=str(liked_flats))
            await db.update_flat(id=int(id), likes=int(likes))
    else:
        likes += 1
        await db.update_user(telegram_id=int(call.from_user.id), liked_id=str(id))
        await db.update_flat(id=int(id), likes=int(likes))

    await likes_dislikes(call, id, likes, dislikes, views, categ, sub1)


async def more_dislikes(call: CallbackQuery, callback_data: dict):
    db = call.message.bot.get("db")
    id = callback_data.get("id")
    likes = int(callback_data.get("likes"))
    dislikes = int(callback_data.get("dislikes"))
    views = int(callback_data.get("views"))
    categ = callback_data.get("categ")
    sub1 = callback_data.get("sub1")

    await call.answer()

    user = await db.select_user(telegram_id=int(call.from_user.id))
    disliked_ids = user.get("disliked_id")
    liked_ids = user.get("liked_id")

    if liked_ids is not None:
        flat_ids = liked_ids.split(",")
        if str(id) in flat_ids:
            flat_ids.remove(str(id))
            likes -= 1
            if len(flat_ids) == 0:
                await db.update_user(telegram_id=int(call.from_user.id), liked_id=None)
            else:
                liked_flats = ",".join(flat_ids)
                await db.update_user(telegram_id=int(call.from_user.id), liked_id=str(liked_flats))
            await db.update_flat(id=int(id), likes=int(likes))
        else:
            pass
    else:
        pass
    if disliked_ids is not None:
        disflat_ids = disliked_ids.split(",")
        if str(id) not in disflat_ids:
            disflat_ids.append(str(id))
            disflat = ",".join(disflat_ids)
            dislikes += 1
            await db.update_user(telegram_id=int(call.from_user.id), disliked_id=str(disflat))
            await db.update_flat(id=int(id), dislikes=int(dislikes))
    else:
        dislikes += 1
        await db.update_user(telegram_id=int(call.from_user.id), disliked_id=str(id))
        await db.update_flat(id=int(id), dislikes=int(dislikes))

    await likes_dislikes(call, id, likes, dislikes, views, categ, sub1)


async def more_views(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = call.message.bot.get("db")
    id = callback_data.get("id")
    views = int(callback_data.get("dislikes"))
    await call.answer()
    await db.update_flat(id=int(id), viewed=int(views))
    if await ru_language(call):
        await call.message.answer("Отправьте ваш номер телефона (9989xxxxxxxx):", reply_markup=phonenumber)
    else:
        await call.message.answer("Telefon raqamingizni yuboring (9989xxxxxxxx):", reply_markup=phonenumber_uz)
    await User.Phone.set()
    await state.update_data(id=id)


# User.Phone
async def info_phone(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    contc = message.contact.phone_number
    data = await state.get_data()
    id = int(data.get("id"))
    await state.reset_state()
    flat = await db.select_flat(id=int(id))
    categ = flat.get("category")
    sub1categ = flat.get("sub1category")
    sub2categ = flat.get("sub2category")
    article_url = flat.get("article_url")
    user = await db.select_user(telegram_id=int(message.from_user.id))
    orders = user.get("orders")
    if orders is None:
        orders = 1
    else:
        orders += 1
    await db.update_user(telegram_id=int(message.from_user.id), orders=orders)

    if await ru_language(message):
        lang = "Русский"
        text1 = "Спасибо за заявку! Ждите звонка от нас"
    else:
        lang = "Узбекский"
        text1 = "Murojaat uchun rahmat! Bizdan qo'ng'iroqni kuting"
    username = await get_name(message.from_user.id, message)
    text = f"Клиент: {username}  {orders}\n" \
           f"Номер телефона: <code>{contc}</code> \n" \
           f"Язык: {lang}\n\n" \
           f"{categ}\n" \
           f"Район: {sub1categ}\n" \
           f"Комнат: {sub2categ}\n" \
           f"Квартира: \n" \
           f"{article_url}"
    inline = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Забрать", callback_data="take")]])
    await message.bot.send_message(-1001886645112, text, reply_markup=inline)
    menu = await admins_list(message)
    await message.answer(text1, reply_markup=menu)


# User.Phone
async def info_phone_text(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    try:
        int(message.text)
        if "9989" in str(message.text) and len(message.text) == 12:
            cont = message.text
            data = await state.get_data()
            id = int(data.get("id"))
            await state.reset_state()
            flat = await db.select_flat(id=int(id))
            categ = flat.get("category")
            sub1categ = flat.get("sub1category")
            sub2categ = flat.get("sub2category")
            article_url = flat.get("article_url")

            user = await db.select_user(telegram_id=int(message.from_user.id))
            orders = user.get("orders")
            if orders is None:
                orders = 1
            else:
                orders += 1
            await db.update_user(telegram_id=int(message.from_user.id), orders=orders)

            if await ru_language(message):
                lang = "Русский"
                text1 = "Спасибо за заявку! Ждите звонка от нас"
            else:
                lang = "Узбекский"
                text1 = "Murojaat uchun rahmat! Bizdan qo'ng'iroqni kuting"
            username = await get_name(message.from_user.id, message)
            text = f"Клиент: {username}  {orders}\n" \
                   f"Номер телефона: <code>{cont}</code> \n" \
                   f"Язык: {lang}\n\n" \
                   f"{categ}\n" \
                   f"Район: {sub1categ}\n" \
                   f"Комнат: {sub2categ}\n" \
                   f"Квартира: \n" \
                   f"{article_url}"
            inline = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Забрать", callback_data="take")]])
            await message.bot.send_message(-1001886645112, text, reply_markup=inline)
            menu = await admins_list(message)
            await message.answer(text1, reply_markup=menu)
        else:
            if await ru_language(message):
                await message.answer("Отправьте ваш номер телефона (9989xxxxxxxx):", reply_markup=phonenumber)
            else:
                await message.answer("Telefon raqamingizni yuboring (9989xxxxxxxx):", reply_markup=phonenumber_uz)
            await User.Phone.set()
    except:
        if await ru_language(message):
            await message.answer("Отправьте ваш номер телефона (9989xxxxxxxx):", reply_markup=phonenumber)
        else:
            await message.answer("Telefon raqamingizni yuboring (9989xxxxxxxx):", reply_markup=phonenumber_uz)
        await User.Phone.set()


async def got_order(call: CallbackQuery):
    message = call.message.text
    text = message + f"\n\n● <b>Забрал заявку на осмотр квартиры: {call.from_user.full_name}</b>\n "
    await call.bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id)


async def get_name(id, message):
    db = message.bot.get("db")
    user = await db.select_user(telegram_id=int(id))
    username = user.get("username")
    first_name = user.get("first_name")
    if username:
        player = f"@{username}"
    else:
        player = f"<a href='tg://user?id={id}'>{first_name}</a>"
    return player


def register_sale(dp: Dispatcher):
    dp.register_message_handler(get_sale_category, text=["Продажа", "Sotiladi"])
    dp.register_message_handler(get_sale_sub1category, state=Flat.Sub1)
    dp.register_message_handler(get_sale_sub2category, state=Flat.Sub2)
    dp.register_callback_query_handler(back_sub1, flat.filter(action="back", categ="Продажа"))
    dp.register_callback_query_handler(more_likes, flat.filter(action="like"))
    dp.register_callback_query_handler(more_dislikes, flat.filter(action="dislike"))
    dp.register_callback_query_handler(more_views, flat.filter(action="view"))
    dp.register_message_handler(info_phone_text, state=User.Phone, content_types=types.ContentType.TEXT)
    dp.register_message_handler(info_phone, state=User.Phone, content_types=types.ContentType.CONTACT)
    dp.register_callback_query_handler(got_order, text="take")




