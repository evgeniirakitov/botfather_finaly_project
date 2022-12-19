import logging

import gino
from sqlalchemy.sql import text

from tgbot.models.table import Item


async def add_item(name: str, description: str, price: int, quantity: int, photo_url: str):
    """
    Adds a new item to the shopping list.

    :param name: The name of the item.
    :param description: The description of the item.
    :param price: The price of the item.
    """
    item = Item(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        photo_url=photo_url
    )

    await item.create()


async def select_item(id: int):
    """
    Selects the item with the given id.

    :param id: The id of the item to select.
    """
    item = await Item.get(id)

    return item


async def select_all_items():
    """
    Selects all items.
    """
    items = await Item.query.gino.all()

    return items


async def select_first_two_items():
    items = await Item.query.order_by(Item.name).limit(2).gino.all()

    return items


async def select_items_by_name(name: str):
    items = await Item.query.where(text(f"{Item.name} LIKE '{name}%'")).gino.all()
    logging.info(f"items = {items}")

    return items


async def update_item(item_id: int, price: int, quantity: int, photo_url: str):
    """
    Updates an item in the shopping list.

    :param item_id: The id of the item.
    :param price: The new price of the item.
    :param quantity: The new quantity of the item.
    :param photo_url: The new photo url of the item.
    """
    item = await Item.get(item_id)
    item.price = price
    item.quantity = quantity
    item.photo_url = photo_url
    await item.save()


async def update_item_price(item_id: int, price: int):
    """
    Updates the price of an item in the shopping list.

    :param item_id: The id of the item.
    :param price: The new price of the item.
    """
    item = await Item.get(item_id)
    item.price = price
    await item.save()


async def update_item_quantity(item_id: int, delta: int):
    """
    Updates the quantity of an item in the shopping list.

    :param item_id: The id of the item.
    :param delta: The new quantity of the item.
    """
    item = await Item.get(item_id)
    item.quantity -= delta
    await item.save()


async def remove_item(id: int):
    """
    Removes an item from the shopping list.

    :param id: The id of the item to remove.
    """
    item = Item.get(id)
    if item:
        await item.delete()
