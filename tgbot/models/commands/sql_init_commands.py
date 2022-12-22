import asyncio

from sqlalchemy import null

from tgbot.config import load_config
from tgbot.models.commands import user_commands, item_commands
from tgbot.models.db_gino import db


async def sql_init():
    config = load_config(".env")

    url = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"

    await db.set_bind(url)

    await user_commands.add_user(123456, "admin", "admin", "admin@admin.com", 0, 123456)

    await item_commands.add_item("ноут", "Описание", 100, 9,
                                 "https://st.depositphotos.com/1001877/1428/i/600/depositphotos_14285099-stock-photo-laptop-3d.jpg")
    await item_commands.add_item("ноут2", "Описание ноут 2", 100, 9,
                                 "https://c.dns-shop.ru/thumb/st4/fit/760/600/0648268dac1af7b409c5e114464b81f3/q93_0eb48f0f85088252c930f01943d4a4ca9e5851dcabd452fd60bc725424013370.jpg")
    await item_commands.add_item("айфон", "Описание айфон ", 100, 9,
                                 "https://www.ixbt.com/img/x780x600/r30/00/02/56/75/cover.jpg")
    await item_commands.add_item("макбук", "Описание макбук", 100, 9,
                                 "https://appleinsider.ru/wp-content/uploads/2017/01/apple-macbook-pro-15-with-touch-bar-hands-on-0004-1500x1000-2.jpg")
