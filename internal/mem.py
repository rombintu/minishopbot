# from internal.database import Category
from random import randint, choice

some_items = ["Скраб", "Тоник", "Средство для лица", "Тушь", "Мыло обычное", "Шампунь какая то марка"]
users = []

def login(uuid):
    user = None
    for u in users:
        if u.uuid == uuid:
            user = u
    if not user:
        user = User(uuid)
        users.append(user)
    return user


class Category:
    def __init__(self, _id, title):
        self._id = _id
        self.title = title
        self.emoji = ""

rand_capacity = ["x1", "400ml", "950ml"] # TODO
class Item:
    def __init__(self, _id, title, category_id, price):
        self._id = _id
        self.title = title
        self.category_id = category_id
        self.price = price
        self.capacity = choice(rand_capacity)

class Basket:
    def __init__(self, uuid):
        self.user_id = uuid
        self.items = []

    def get_items(self):
        return self.items

    def sum(self):
        s = 0
        for item in self.get_items():
            s += item.price
        return s

    def get_content(self):
        if not self.get_items():
            return "Корзина пуста"
        else:
            return f"Итого: {self.sum()} ₽"

    def add_items(self, item):
        self.items.append(item)


class User:
    def __init__(self, uuid):
        self.uuid = uuid
        self.basket = Basket(self.uuid)

    def to_basket(self, item):
        self.basket.add_items(item)

    def get_basket(self):
        return self.basket 

class Menu:
    categories = []
    items = []

    def __init__(self):
        self.refresh_categories()
        self.categories[3].emoji = "🎁"
        self.refresh_items()

    def refresh_categories(self):
        self.categories = [Category(i, f"category_{i}") for i in range(0, 12)] # TODO
        self.categories[3].emoji = "🎁"

    def refresh_items(self):
        self.items = [Item(i, f"{choice(some_items)}", 3, randint(200, 2500)) for i in range(0, 19)] # TODO

    # TODO
    def get_cat_by_id(self, category_id):
        for c in self.categories:
            if c._id == category_id:
                return c

    # TODO
    def get_items_by_category_id(self, category_id):
        payload = []
        for item in self.items:
            if item.category_id == category_id:
                payload.append(item)
        return payload

    # TODO
    def get_item_by_id(self, category_id, _id):
        for item in self.items:
            if item.category_id == category_id and item._id == _id:
                return item


menu = Menu()