from sqlalchemy import String

from tgbot.models.db_gino import TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(String(100), nullable=False)
    user_name = db.Column(String(100))
    email = db.Column(String(100))

    referrer = db.Column(db.BigInteger, nullable=False)

    balance = db.Column(db.BigInteger, nullable=True)


class Item(TimedBaseModel):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    photo_url = db.Column(db.String, nullable=False)


class Order(TimedBaseModel):
    __tablename__ = 'basket'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE")


class OrderItem(TimedBaseModel):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True),

    product_id = db.Column(db.Integer,
                           db.ForeignKey(f"{Order.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"))
    items_id = db.Column(db.Integer, db.ForeignKey(f"{Item.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"))
