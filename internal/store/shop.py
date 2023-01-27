
from pymongo import MongoClient
from datetime import datetime
from internal.logger import new_logger 
from bson import ObjectId

class User:
    def __init__(self, uuid=0, username="", _id=ObjectId()):
        self._id = _id
        self.uuid = uuid
        self.username = username
        self.basket = Basket(self.uuid)

    def to_basket(self, element):
        self.basket.add_element(element)

    def get_basket(self):
        return self.basket 


class Category:
    def __init__(self, title, emoji, _id=ObjectId()):
        self._id = _id
        self.title = title
        self.emoji = emoji

class Item:
    def __init__(
            self, title="", category_title="",
            price=0, capacity="x1", picture="", 
            description="", _id=ObjectId()
        ):
        self._id = _id
        self.title = title
        self.category_title = category_title
        # self.category_id = category_id
        self.price = price
        self.capacity = capacity
        self.stars = 0
        self.picture = picture
        self.description = description

class Basket:
    def __init__(self, uuid):
        self.user_id = uuid
        self.elements = []

    def get_elements(self):
        return self.elements

    def sum(self):
        s = 0
        for item in self.get_elements():
            s += item["data"].price * item["count"]
        return s

    def get_content(self):
        if not self.get_elements():
            return "Корзина пуста"
        else:
            return f"Итого: {self.sum()} ₽"

    def add_element(self, elem: Item):
        for el in self.get_elements():
            if el["id"] == elem._id:
                el["count"] += 1
                return
        self.elements.append(
            {
            "id": elem._id,
            "data": elem,
            "count": 1,
            }
        )
    # def remove_element(self, _id):
    #     for el in self.get_elements():
    #         if el["id"] == _id:
                
    
    def clear(self):
        self.elements = []

class Order(Basket):
    def __init__(self, uuid):
        super().__init__(uuid)
        self.create_at = datetime.now()
        self.completed_at = None

class Shop:
    categories = []
    items = []
    users = []

    def __init__(self, connection):
        self.store = MongoClient(connection)["minishop"]
        self.refresh_categories()
        self.refresh_items()

    def get_categories(self):
        return self.categories
    def get_items(self):
        return self.items

    def get_user_from_mem(self, user):
        for u in self.users:
            if u.uuid == user.uuid:
                return u
        return None

    def login(self, user: User):
        data = self.store.users.find_one({"uuid": user.uuid})
        if not self.get_user_from_mem(user):
            self.users.append(user)
        if not data:
            self.store.users.insert_one({
                "_id": user._id,
                "uuid": user.uuid,
                "username": user.username,
            })
        return self.get_user_from_mem(user)

    def user_order_create(self, user: User):
        order = Order(User.get_basket())
        self.store.orders.insert_one(order.__dict__)
        user.basket.clear()
        return user
    
    # TODO
    def user_order_competed(self, order_id):
        pass

    def category_create(self, c: Category):
        self.store.categories.insert_one({
            "title": c.title, "emoji": c.emoji
        })

    def item_create(self, i: Item):
        self.store.items.insert_one({
            "title": i.title, "category_title": i.category_title,
            "price": i.price, "capacity": i.capacity, "stars": i.stars
        })

    def category_delete(self, _id):
        self.store.categories.delete_one({"_id": _id})

    def item_delete(self, _id):
        self.store.items.delete_many({"_id": _id})

    def refresh_categories(self):
        categories = []
        for c in self.store.categories.find():
            categories.append(Category(**c))
        self.categories = categories

    def refresh_items(self):
        items = []
        for i in self.store.items.find():
            items.append(Item(**i))
        self.items = items

    # TODO
    def get_cat_by_id(self, category_id):
        for c in self.categories:
            if c._id == ObjectId(category_id):
                return c
        return None

    # TODO
    def get_items_by_category_id(self, category_title):
        payload = []
        for item in self.items:
            if item.category_title == category_title:
                payload.append(item)
        return payload

    # TODO
    def get_item_by_id(self, category_title, _id):
        for item in self.items:
            if item.category_title == category_title \
                    and item._id == ObjectId(_id):
                return item
        return None

