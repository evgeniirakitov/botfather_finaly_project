from sqlalchemy import Column, BigInteger, String, sql

from tgbot.models.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    referrer = Column(String(100), nullable=False)

    query = sql.Select