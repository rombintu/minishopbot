
from pymongo import MongoClient

class User:
    def __init__(self, uuid, username="", basket=[]):
        self.uuid = uuid
        self.username = username
        if not basket:
            self.basket = Basket(self.uuid)
        else:
            self.basket = basket

    def to_basket(self, item):
        self.basket.add_items(item)

    def get_basket(self):
        return self.basket 

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

class Category:
    def __init__(self, title, emoji=""):
        # self._id = _id
        self.title = title
        self.emoji = emoji

class Item:
    def __init__(self, title, category_id, price, capacity="x1"):
        # self._id = _id
        self.title = title
        self.category_id = category_id
        self.price = price
        self.capacity = capacity

class Shop:
    categories = []
    items = []

    def __init__(self, connection):
        self.store = MongoClient(connection)["minishop"]
        self.refresh_categories()
        self.refresh_items()

    def login(self, uuid: int, username=""):
        data = self.store.users.find_one({"uuid": uuid})
        if not data:
            self.store.users.insert_one({
                "uuid": uuid,
                "username": username
            })
        return User(uuid, username)

    def category_create(self, category: Category):
        data = self.store.categories.find_one({"title": category.title})
        if not data:
            self.store.categories.insert_one({
                "title": category.title,
                "emoji": category.emoji
            })
        return data

    def category_delete(self, title):
        self.store.categories.delete_one({"title": title})

    def item_create(self, item: Item):
        data = self.store.items.find_one({"title": item.title})
        print(data)
        if not data:
            self.store.items.insert_one({
                "title": item.title,
                "category_id": item.category_id,
                "price": item.price,
                "capacity": item.capacity
            })
        return data

    def item_delete(self, title):
        self.store.items.delete_one({"title": title})

    def refresh_categories(self):
        categories = []
        for c in self.store.categories.find():
            categories.append(c)
        self.categories = categories

    def refresh_items(self):
        items = []
        for c in self.store.items.find():
            items.append(c)
        self.items = items

    # TODO
    def get_cat_by_id(self, category_id):
        for c in self.categories:
            if c._id == category_id:
                return c
        return None

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
        return None