from tgbot.models.table import User


async def select_referrals(id: int):
    referrals = await User.query.where(User.referrer == id).gino.all()
    return referrals
