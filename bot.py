import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.db_api.postgresql import Database
from tgbot.config import load_config
from tgbot.filters.is_admin import IsAdmin, IsGroup, IsAdmin_1
from tgbot.handlers.admins.add_admin import register_add_admin
from tgbot.handlers.admins.custom_admins import register_custom_admins
from tgbot.handlers.admins.custom_flat import register_custom_flat
from tgbot.handlers.admins.delete_flat import register_delete_flat
from tgbot.handlers.admins.edit_flat import register_edit_flat
from tgbot.handlers.users.about import register_adout
from tgbot.handlers.users.rent import register_rent
from tgbot.handlers.users.sale import register_sale
from tgbot.handlers.users.start import register_start
from tgbot.middlewares.language_mid import setup_middleware
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_filters(dp):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsAdmin_1)
    dp.filters_factory.bind(IsGroup)


def register_all_handlers(dp):
    register_start(dp)

    register_custom_admins(dp)
    register_add_admin(dp)
    register_custom_flat(dp)
    register_delete_flat(dp)
    register_edit_flat(dp)

    register_sale(dp)
    register_rent(dp)
    register_adout(dp)


async def main():
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    db = Database()
    i18n = setup_middleware(dp)
    lang = i18n.gettext

    bot['config'] = config
    bot['lang'] = lang

    register_all_filters(dp)
    register_all_handlers(dp)

    await db.create()

    # await db.drop_users()
    # await db.drop_admins()
    # await db.drop_flats()

    await db.create_table_users()
    await db.create_table_flats()
    await db.create_table_admins()

    bot['db'] = db

    await set_default_commands(dp)
    await on_startup_notify(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
