import asyncio

from sqlalchemy import null

from tgbot.models.commands import user_commands, item_commands
from tgbot.models.db_gino import db


async def sql_init():
    await db.set_bind("postgresql://postgres:akitov2009@localhost:5432/postgres")


    await item_commands.add_item("ноут", "Описание", 100, 9, "")
