from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.admins.custom_admins import cancel_admin
from tgbot.handlers.users.start import bot_start, admins_list
from tgbot.keyboards.default.main_menu import m_menu
from tgbot.states.users import Admin


customize = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить Админа"),
            KeyboardButton(text="Удалить Админа"),
        ],
        [
            KeyboardButton(text="Главное Меню")
        ]
    ],
    resize_keyboard=True
)


async def list_admins(message: types.Message):
    await message.answer("Что вы хотите сделать ?", reply_markup=customize)


async def add_admin(message: types.Message):
    db = message.bot.get('db')
    await message.answer("Введите айди пользователя которого хотите добавить в администраторы\n\n"
                         "Потенциальный админ должен у себя в боте отправить команду /get_my_id")
    text = f"Все Админы:\n\n"
    for id, telegram_id, name, level in await db.select_all_admins():
        text += f"{name} - {telegram_id}\n"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Отменить"))
    await message.answer(text, reply_markup=markup)
    await Admin.Add_admin.set()


# Admin.Add_admin
async def add_admin_1(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    potential_admin = message.text
    admin = message.from_user.id
    if message.text == "Отменить":
        await cancel_admin(message, state)
    else:
        await state.reset_state(with_data=False)
        try:
            int(potential_admin)
            user_in_db = await db.select_user(telegram_id=int(potential_admin))
            try:
                poten = user_in_db.get("telegram_id")
                if int(potential_admin) != int(admin) and int(potential_admin) == int(poten):
                    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    markup.insert(KeyboardButton(text="Назад"))
                    markup.insert(KeyboardButton(text="Уровень 1"))
                    markup.insert(KeyboardButton(text="Уровень 2"))
                    await message.answer("Отправьте уровень потенциального админа", reply_markup=markup)
                    await Admin.Add_level.set()
                    await state.update_data(poten_id=int(poten))
                else:
                    await message.answer(f"<b>Вы уже являетесь админом!</b>", reply_markup=customize)
            except:
                await message.answer("<b>В базе нет такого пользователя!</b>", reply_markup=customize)
        except ValueError:
            await message.answer("<b>Пожалуйста!</b> Введите айди пользователя", reply_markup=customize)


# Admin.Add_level
async def add_level_admin(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    menu = await admins_list(message)
    admin_name = message.from_user.full_name
    data = await state.get_data()
    poten_id = int(data.get("poten_id"))
    user_in_db = await db.select_user(telegram_id=int(poten_id))
    poten_name = user_in_db.get("first_name")
    if message.text == "Назад":
        await state.reset_state()
        await add_admin(message)
    elif message.text == "Уровень 1":
        await state.reset_state()
        try:
            await db.add_administrator(telegram_id=int(poten_id), name=poten_name, level=1)
            await message.answer(f"Вы добавили в админы пользователя {poten_name}", reply_markup=menu)
            await message.bot.send_message(int(poten_id),
                                           f"Вы были добавлены в админы пользователем {admin_name}",
                                           reply_markup=menu)
        except Exception as err:
            print(err)
            await message.answer("<b>Этот пользователь уже добавлен в админы!</b>",
                                 reply_markup=customize)
    elif message.text == "Уровень 2":
        await state.reset_state()
        try:
            await db.add_administrator(telegram_id=int(poten_id), name=poten_name, level=2)
            await message.answer(f"Вы добавили в админы пользователя {poten_name}", reply_markup=menu)
            await message.bot.send_message(int(poten_id),
                                           f"Вы были добавлены в админы пользователем {admin_name}",
                                           reply_markup=menu)
        except Exception as err:
            print(err)
            await message.answer("<b>Этот пользователь уже добавлен в админы!</b>",
                                 reply_markup=customize)
    else:
        pass


async def delete_admin(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    text = f"Все Админы:\n\n"
    for id, telegram_id, name, level in await db.select_all_admins():
        text += f"{name} - {telegram_id}\n"
    await message.answer(text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton(text="Отменить"))
    for id, telegram_id, name, level in await db.select_all_admins():
        markup.insert(KeyboardButton(text=name))
    await message.answer("Выберите админа которого хотите удалить из администраторов", reply_markup=markup)
    await Admin.Delete_admin.set()


# Admin.Delete_admin
async def delete_admin_1(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    menu = await admins_list(message)
    if message.text == "Отменить":
        await cancel_admin(message, state)
    else:
        try:
            select = await db.select_admin(name=message.text)
            telegram_id = select.get("telegram_id")
            await db.delete_admin(telegram_id=int(telegram_id))
            await message.answer(f"Админ {message.text} успешно удален из администраторов", reply_markup=menu)
            await message.bot.send_message(int(telegram_id),
                                           f"Вы были  удалены из администраторов пользователем {message.from_user.full_name}",
                                           reply_markup=m_menu)
            await state.reset_state()
        except:
            await message.answer("<b>В базе нет такого пользователя!</b>", reply_markup=customize)
            await state.reset_state()


async def get_id(message: types.Message, state: FSMContext):
    await message.answer(f"Ваш айди: {message.from_user.id}")


async def number_users(message: types.Message, state: FSMContext):
    db = message.bot.get('db')
    count_users = await db.count_users()
    await message.answer(f"Количество пользователей: {count_users}")


async def add_owner(message: types.Message):
    db = message.bot.get('db')
    await db.add_administrator(telegram_id=int(153479611), name="Мухаммад", level=1)


def register_add_admin(dp: Dispatcher):
    dp.register_message_handler(list_admins, IsAdmin(), text="Админы")
    dp.register_message_handler(add_admin, IsAdmin(), text="Добавить Админа")
    dp.register_message_handler(delete_admin, IsAdmin(), text="Удалить Админа")
    dp.register_message_handler(add_admin_1, state=Admin.Add_admin)
    dp.register_message_handler(add_level_admin, state=Admin.Add_level)
    dp.register_message_handler(delete_admin_1, state=Admin.Delete_admin)
    dp.register_message_handler(get_id, Command("get_my_id"))
    dp.register_message_handler(number_users, Command("all_users"), IsAdmin())
    dp.register_message_handler(add_owner, Command("add_owner"))





