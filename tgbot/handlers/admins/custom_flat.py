from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.users.start import bot_start, admins_list
from tgbot.keyboards.default.cancel import cancel, back
from tgbot.keyboards.default.confirm import confirm
from tgbot.keyboards.default.cust_flat import flat_customize, flat_customize_adm
from tgbot.states.users import Admin, Add_Flat, Add_Room


async def custom_flat(message):
    db = message.bot.get("db")
    admins_1 = []
    admins_2 = []
    for id, telegram_id, name, level in await db.select_all_admins():
        if level ==1:
            admins_1.append(telegram_id)
        if level == 2:
            admins_2.append(telegram_id)
    if message.from_user.id in admins_1:
        cust_flat = flat_customize_adm
    else:
        cust_flat = flat_customize
    return cust_flat


async def custom_flats(message: types.Message):
    cust_flat = await custom_flat(message)
    await message.answer("Что вы хотите сделать ?", reply_markup=cust_flat)


async def add_flat(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Продажа"))
    markup.insert(KeyboardButton(text="Аренда"))
    markup.insert(KeyboardButton(text="Главное Меню"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Выберите категорию:", reply_markup=markup)
    await Add_Flat.Categ.set()


async def areas(message, state, categ):
    db = message.bot.get("db")
    sub1categories = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Добавить район"))
    markup.insert(KeyboardButton(text="Назад"))
    for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_category(
            category=categ):
        if sub1category not in sub1categories:
            sub1categories.append(sub1category)
            markup.insert(KeyboardButton(text=sub1category))
    await state.update_data(categ=categ)
    await message.answer(f"Выберите район либо добавьте новый", reply_markup=markup)
    await Add_Flat.Sub1.set()


async def rooms(message, state, categ, sub1categ):
    db = message.bot.get("db")
    try:
        select = await db.select_flat(sub1category=sub1categ, category=categ)
        select.get("sub2category")
        sub1_codee = select.get("sub1_code")
        sub2categories = []
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новое кол-во"))
        markup.insert(KeyboardButton(text="Назад"))
        for id, category, sub1_code, sub1category, sub1category_uz, sub2category, sub2category_uz, article_url, article_url_uz, like, dislike, viewed in await db.select_in_sub1category(
                category=categ, sub1category=sub1categ):
            if sub2category not in sub2categories:
                sub2categories.append(sub2category)
        for room in sorted(sub2categories):
            markup.insert(KeyboardButton(text=room))
        await message.answer(f"Выберите количество комнат либо добавить новое кол-во", reply_markup=markup)
        await state.update_data(sub1=sub1categ)
        await state.update_data(sub1_code=sub1_codee)
        await Add_Flat.Sub2.set()
    except:
        pass


# Add_Flat.Categ
async def select_in_categ(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.reset_state()
        await custom_flats(message)
    else:
        await areas(message, state, message.text)


# Add_Flat.Sub1
async def select_in_sub1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    categ = data.get("categ")
    if message.text == "Добавить район":
        await message.answer("Отправьте название района", reply_markup=back)
        await Add_Flat.New_sub1.set()
    elif message.text == "Назад":
        await state.reset_state()
        await add_flat(message, state)
    else:
        await rooms(message, state, categ, message.text)


# Add_Flat.Sub2
async def select_in_sub2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    sub1 = data.get("sub1")
    if message.text == "Добавить новое кол-во":
        await state.reset_state()
        await message.answer("Отправьте новое кол-во комнат", reply_markup=back)
        await Add_Room.New_sub2.set()
        await state.update_data(categ=categ)
        await state.update_data(sub1=sub1)
    elif message.text == "Назад":
        await areas(message, state, categ)
    else:
        try:
            select = await db.select_flat(sub2category=message.text)
            select.get("article_url")
            await message.answer("Отправьте ссылку на статью с квартирой", reply_markup=back)
            await state.update_data(sub2=message.text)
            await Add_Flat.Url.set()
        except:
            # await state.reset_state()
            # await add_flat(message)
            pass


# Add_Flat.Url
async def add_flat_url(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        data = await state.get_data()
        categ = data.get("categ")
        sub1 = data.get("sub1")
        await rooms(message, state, categ, sub1)
    else:
        await message.answer("Отправьте ссылку на статью с квартирой для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(url=message.text)
        await Add_Flat.Url_uz.set()


# Add_Flat.Url_uz
async def add_flat_url_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    # print(state.get_data())
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на статью с квартирой", reply_markup=back)
        await Add_Flat.Url.set()
    else:
        await state.update_data(url_uz=message.text)
        data = await state.get_data()
        categ = data.get("categ")
        sub1 = data.get("sub1")
        sub2 = data.get("sub2")
        url = data.get("url")
        url_uz = message.text
        sub1_db = await db.select_flat(sub1category=sub1)
        sub1_uz = sub1_db.get("sub1category_uz")
        sub2_db = await db.select_flat(sub2category=sub2)
        sub2_uz = sub2_db.get("sub2category_uz")
        await state.update_data(sub1_uz=sub1_uz)
        await state.update_data(sub2_uz=sub2_uz)
        text = f"Категория: {categ}\n" \
               f"Район: {sub1}/{sub1_uz}\n" \
               f"Комнат: {sub2}/{sub2_uz}\n\n" \
               f"Ссылка на статью с квартирой для русскоязычных пользователей: \n" \
               f"{url}"
        await message.answer(text)
        text1 = f"Ссылка на статью с квартирой для узбекоязычных пользователей: \n" \
                f"{url_uz}"
        await message.answer(text1)
        await message.answer("Все верно?", reply_markup=confirm)
        await Add_Flat.Confirm.set()


# Add_Flat.Confirm
async def add_flat_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if message.text == "Верно":
        data = await state.get_data()
        categ = data.get("categ")
        sub1_code = data.get("sub1_code")
        sub1 = data.get("sub1")
        sub1_uz = data.get("sub1_uz")
        sub2 = data.get("sub2")
        sub2_uz = data.get("sub2_uz")
        url = data.get("url")
        url_uz = data.get("url_uz")
        await db.add_flat(category=categ, sub1_code=sub1_code, sub1category=sub1, sub1category_uz=sub1_uz, sub2category=sub2, sub2category_uz=sub2_uz, article_url=url, article_url_uz=url_uz, likes=0, dislikes=0, viewed=0)
        menu = await admins_list(message)
        await message.answer("Квартира была добавлена в базу данных!", reply_markup=menu)
        await state.reset_state()
    elif message.text == "Назад":
        await message.answer("Отправьте ссылку на статью с квартирой для узбекоязычных пользователей", reply_markup=back)
        await Add_Flat.Url_uz.set()
    elif message.text == "Отменить":
        await state.reset_state()
        await add_flat(message, state)
    else:
        pass

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Add_Flat.New_sub1
async def add_sub1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if message.text == "Назад":
        data = await state.get_data()
        categ = data.get("categ")
        await areas(message, state, categ)
    else:
        await message.answer("Отправьте название района для узбекоязычных пользователей", reply_markup=back)
        sub1_codes = await db.select_sub1()
        max_sub1_code = max(sub1_codes, key=lambda x: x)
        new_sub1 = 1 + int(max_sub1_code.get("sub1_code"))
        await state.update_data(sub1=message.text)
        await state.update_data(sub1_code=new_sub1)
        await Add_Flat.New_sub1_uz.set()


# Add_Flat.New_sub1_uz
async def add_sub1_uz(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отправьте название района")
        await Add_Flat.New_sub1.set()
    else:
        await message.answer("Отправьте кол-во комнат", reply_markup=back)
        await state.update_data(sub1_uz=message.text)
        await Add_Flat.New_sub2.set()


# Add_Flat.New_sub2
async def add_sub2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отправьте название района для узбекоязычных пользователей", reply_markup=back)
        await Add_Flat.New_sub1_uz.set()
    else:
        await message.answer("Отправьте кол-во комнат для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(sub2=message.text)
        await Add_Flat.New_sub2_uz.set()


# Add_Flat.New_sub2_uz
async def add_sub2_uz(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отправьте кол-во комнат", reply_markup=back)
        await Add_Flat.New_sub2.set()
    else:
        await message.answer("Отправьте ссылку на статью с квартирой", reply_markup=back)
        await state.update_data(sub2_uz=message.text)
        await Add_Flat.New_url.set()


# Add_Flat.New_url
async def add_url(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отправьте кол-во комнат для узбекоязычных пользователей", reply_markup=back)
        await Add_Flat.New_sub2_uz.set()
    else:
        await message.answer("Отправьте ссылку на статью с квартирой для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(url=message.text)
        await Add_Flat.New_url_uz.set()


# Add_Flat.New_url_uz
async def add_url_uz(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на статью с квартирой", reply_markup=back)
        await Add_Flat.New_url.set()
    else:
        await state.update_data(url_uz=message.text)
        data = await state.get_data()
        categ = data.get("categ")
        sub1_code = data.get("sub1_code")
        sub1 = data.get("sub1")
        sub1_uz = data.get("sub1_uz")
        sub2 = data.get("sub2")
        sub2_uz = data.get("sub2_uz")
        url = data.get("url")
        url_uz = message.text
        text = f"Категория: {categ}\n" \
               f"Район: {sub1}/{sub1_uz}\n" \
               f"Комнат: {sub2}/{sub2_uz}\n\n" \
               f"Ссылка на статью с квартирой для русскоязычных пользователей: \n" \
               f"{url}"
        await message.answer(text)
        text1 = f"Ссылка на статью с квартирой для узбекоязычных пользователей: \n" \
                f"{url_uz}"
        await message.answer(text1)
        await message.answer("Все верно?", reply_markup=confirm)
        await Add_Flat.New_Confirm.set()


# Add_Flat.New_Confirm
async def add_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if message.text == "Верно":
        data = await state.get_data()
        categ = data.get("categ")
        sub1_code = data.get("sub1_code")
        sub1 = data.get("sub1")
        sub1_uz = data.get("sub1_uz")
        sub2 = data.get("sub2")
        sub2_uz = data.get("sub2_uz")
        url = data.get("url")
        url_uz = data.get("url_uz")
        await db.add_flat(category=categ, sub1_code=sub1_code, sub1category=sub1, sub1category_uz=sub1_uz, sub2category=sub2, sub2category_uz=sub2_uz, article_url=url, article_url_uz=url_uz, likes=0, dislikes=0, viewed=0)
        menu = await admins_list(message)
        await message.answer("Квартира была добавлена в базу данных!", reply_markup=menu)
        await state.reset_state()
    elif message.text == "Назад":
        await message.answer("Отправьте ссылку на статью с квартирой для узбекоязычных пользователей", reply_markup=back)
        await Add_Flat.New_url_uz.set()
    elif message.text == "Отменить":
        await state.reset_state()
        await add_flat(message, state)
    else:
        pass

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Add_Room.New_sub2
async def add_room(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        data = await state.get_data()
        categ = data.get("categ")
        sub1 = data.get("sub1")
        await rooms(message, state, categ, sub1)
    else:
        await message.answer("Отправьте кол-во комнат для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(sub2=message.text)
        await Add_Room.New_sub2_uz.set()


# Add_Room.New_sub2_uz
async def add_room_uz(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        data = await state.get_data()
        categ = data.get("categ")
        sub1 = data.get("sub1")
        await state.reset_state()
        await message.answer("Отправьте новое кол-во комнат")
        await Add_Room.New_sub2.set()
        await state.update_data(categ=categ)
        await state.update_data(sub1=sub1)
    else:
        await message.answer("Отправьте ссылку на статью с квартирой", reply_markup=back)
        await state.update_data(sub2_uz=message.text)
        await Add_Room.New_url.set()


# Add_Room.New_url
async def add_room_url(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отправьте кол-во комнат для узбекоязычных пользователей", reply_markup=back)
        await Add_Room.New_sub2_uz.set()
    else:
        await message.answer("Отправьте ссылку на статью с квартирой для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(url=message.text)
        await Add_Room.New_url_uz.set()


# Add_Room.New_url_uz
async def add_room_url_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на статью с квартирой", reply_markup=back)
        await Add_Room.New_url.set()
    else:
        await state.update_data(url_uz=message.text)
        data = await state.get_data()
        categ = data.get("categ")
        sub1 = data.get("sub1")
        sub1_db = await db.select_flat(sub1category=sub1)
        sub1_uz = sub1_db.get("sub1category_uz")
        sub1_codee = sub1_db.get("sub1_code")
        sub2 = data.get("sub2")
        sub2_uz = data.get("sub2_uz")
        url = data.get("url")
        url_uz = message.text
        await state.update_data(sub1_uz=sub1_uz)
        await state.update_data(sub1_code=sub1_codee)
        text = f"Категория: {categ}\n" \
               f"Район: {sub1}/{sub1_uz}\n" \
               f"Комнат: {sub2}/{sub2_uz}\n\n" \
               f"Ссылка на статью с квартирой для русскоязычных пользователей: \n" \
               f"{url}"
        await message.answer(text)
        text1 = f"Ссылка на статью с квартирой для узбекоязычных пользователей: \n" \
                f"{url_uz}"
        await message.answer(text1)
        await message.answer("Все верно?", reply_markup=confirm)
        await Add_Room.Confirm.set()


# Add_Room.Confirm
async def add_room_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    if message.text == "Верно":
        data = await state.get_data()
        categ = data.get("categ")
        sub1_code = data.get("sub1_code")
        sub1 = data.get("sub1")
        sub1_uz = data.get("sub1_uz")
        sub2 = data.get("sub2")
        sub2_uz = data.get("sub2_uz")
        url = data.get("url")
        url_uz = data.get("url_uz")
        await db.add_flat(category=categ, sub1_code=sub1_code, sub1category=sub1, sub1category_uz=sub1_uz, sub2category=sub2, sub2category_uz=sub2_uz, article_url=url, article_url_uz=url_uz, likes=0, dislikes=0, viewed=0)
        await state.reset_state()
        menu = await admins_list(message)
        await message.answer("Квартира была добавлена в базу данных!", reply_markup=menu)
    elif message.text == "Назад":
        await message.answer("Отправьте ссылку на статью с квартирой для узбекоязычных пользователей", reply_markup=back)
        await Add_Room.New_url_uz.set()
    elif message.text == "Отменить":
        await state.reset_state()
        await add_flat(message, state)
    else:
        pass


def register_custom_flat(dp: Dispatcher):
    dp.register_message_handler(custom_flats, IsAdmin(), text="Квартиры")
    dp.register_message_handler(add_flat, IsAdmin(), text="Добавить Квартиру")
    dp.register_message_handler(select_in_categ, IsAdmin(), state=Add_Flat.Categ, text=["Продажа", "Аренда", "Назад"])
    dp.register_message_handler(select_in_sub1, state=Add_Flat.Sub1)
    dp.register_message_handler(select_in_sub2, state=Add_Flat.Sub2)
    dp.register_message_handler(add_flat_url, state=Add_Flat.Url)
    dp.register_message_handler(add_flat_url_uz, state=Add_Flat.Url_uz)
    dp.register_message_handler(add_flat_confirm, state=Add_Flat.Confirm)

    dp.register_message_handler(add_sub1, state=Add_Flat.New_sub1)
    dp.register_message_handler(add_sub1_uz, state=Add_Flat.New_sub1_uz)
    dp.register_message_handler(add_sub2, state=Add_Flat.New_sub2)
    dp.register_message_handler(add_sub2_uz, state=Add_Flat.New_sub2_uz)
    dp.register_message_handler(add_url, state=Add_Flat.New_url)
    dp.register_message_handler(add_url_uz, state=Add_Flat.New_url_uz)
    dp.register_message_handler(add_confirm, state=Add_Flat.New_Confirm)


    dp.register_message_handler(add_room, state=Add_Room.New_sub2)
    dp.register_message_handler(add_room_uz, state=Add_Room.New_sub2_uz)
    dp.register_message_handler(add_room_url, state=Add_Room.New_url)
    dp.register_message_handler(add_room_url_uz, state=Add_Room.New_url_uz)
    dp.register_message_handler(add_room_confirm, state=Add_Room.Confirm)







