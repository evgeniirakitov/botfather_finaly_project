from asyncpg import UniqueViolationError

from tgbot.models.user import User


async def add_user(id: int, name: str, email: str):
    try:
        user = User(id=id, name=name, email=email).save()
        await user.create()

    except UniqueViolationError:
        pass


async def select_all_user():
    users = await User.select().gino.all()

    return users


async def select_user_by_id(id: int):
    user = await User.query.where(User.id == id).gino.first()

    return user


async def count_users():
    count = await User.query.gino.count(User.id).gino.scalar()
    return count

async def update_user(id: int, email: str):
    user = await User.get(id)

    await user.update(email=email).apply()
