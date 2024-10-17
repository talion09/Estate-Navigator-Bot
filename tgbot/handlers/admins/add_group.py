from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.filters.is_admin import IsAdmin, IsGroup


async def groups(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Добавить группу"))
    markup.insert(KeyboardButton(text="Назад"))
    text = "Если вы хотите чтобы записи скидывались вам в группу, то отправьте в группу команду /show_entries\n\n\n" \
           "Что вы хотите сделать ?"
    await message.answer(text, reply_markup=markup)


async def add_group(message: types.Message):
    bot_name = await message.bot.get_me()
    url = f"t.me/{bot_name.username}?startgroup=true"
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="Добавить", url=url))
    await message.answer("Добавьте бота в свою группу", reply_markup=markup)


async def show_entries(message: types.Message):
    db = message.bot.get("db")
    try:
        await db.add_group(group_id=int(message.chat.id), group_name=message.chat.full_name)
        await message.answer("Теперь в этой группе будут отображаться записи!")
    except:
        group = await db.select_group(group_id=int(message.chat.id))
        try:
            group.get("group_id")
            await message.answer("В этой группе уже отображаются записи!")
        except:
            await message.answer("Ошибка! Напишите разработчику!")


def register_add_group(dp: Dispatcher):
    dp.register_message_handler(groups, IsAdmin(), text="Группы")
    dp.register_message_handler(add_group, IsAdmin(), text="Добавить группу")
    dp.register_message_handler(show_entries, IsAdmin(), IsGroup(), Command("show_entries"))
