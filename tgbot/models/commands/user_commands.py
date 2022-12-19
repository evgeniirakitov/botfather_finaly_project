from asyncpg import UniqueViolationError

from tgbot.models.db_gino import db
from tgbot.models.table import User


async def add_user(id: int, name: str, user_name: str, email: str, balance: int, referrer: int):
    try:

        user = User(
            id=id,
            name=name,
            user_name=user_name,
            email=email,
            balance=balance,
            referrer=referrer
        )
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_user():
    users = await User.query.gino.all()

    return users


async def select_referrals(id: int):
    users = await User.query.where(User.referrer == id).gino.all()

    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()

    return user


async def get_balance(id: int):
    user = await User.query.where(User.id == id).gino.first()

    return user.balance


async def count_users():
    count = await db.func.count(User.id).gino.scalar()
    return count


async def update_user(id: int, email=None, balance=None):
    user = await User.get(id)
    if email is not None and balance is not None:
        await user.update(email=email, balance=balance).apply()
    elif email is not None and balance is None:
        await user.update(email=email).apply()
    else:
        await user.update(balance=balance).apply()
