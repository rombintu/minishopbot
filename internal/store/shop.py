
from pymongo import MongoClient
from datetime import datetime
from internal.logger import new_logger 
from bson import ObjectId
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

class Category:
    def __init__(self, title, emoji, _id=ObjectId()):
        self._id = _id
        self.title = title
        self.emoji = emoji

class Item:
    def __init__(
            self, title="", category_title="",
            price=0, capacity="x1", photo="", 
            description="", stars=0, _id=ObjectId()
        ):
        self._id = _id
        self.title = title
        self.category_title = category_title
        # self.category_id = category_id
        self.price = price
        self.capacity = capacity
        self.stars = stars
        self.photo = photo
        self.description = description

class Basket:
    def __init__(self, uuid):
        self.user_id = uuid
        self.elements = []

    def get_elements(self):
        return self.elements

    def get_elements_ids(self):
        return [
            {
                'i_id': str(elem["id"]), 
                'i_title': elem["data"].title, 
                'i_count': elem["count"],
                'i_sum': elem["data"].price * elem["count"]
            } for elem in self.get_elements()]

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

    def remove(self, element_id: Item):
        for i, el in enumerate(self.get_elements()):
            if el["id"] == ObjectId(element_id):
                self.elements.pop(i)
    # def remove_element(self, _id):
    #     for el in self.get_elements():
    #         if el["id"] == _id:
                
    
    def clear(self):
        self.elements = []

class Order:
    def __init__(self, uuid, items):
        self.uuid = uuid
        self.items = items
        self.created_at = datetime.now()
        self.completed_at = None
        self.sum = 0
        for i in self.items:
            self.sum += i["i_sum"]

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

    def create_order(self):
        if not (self.get_basket()):
            return None
        return Order(self.uuid, self.get_basket().get_elements_ids())

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
            "price": i.price, "capacity": i.capacity, "stars": i.stars,
            "photo": i.photo, "description": i.description
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

    def get_orders_info(self, uuid):
        orders = self.store.orders.find({"uuid": uuid})
        all_orders = []
        if not orders:
            return all_orders
        for o in orders:
            buff = f"Заказ №`{str(o['_id'])}`\n"
            buff += f"Создан _{o['created_at'].strftime('%d.%m.%Y %H:%M')}_\n"
            buff += "Статус: "
            buff += "*В работе*" if not o["completed_at"] else f"*Закрыт* {o['completed_at'].strftime('%d.%m.%Y %H:%M')}" 
            for i in  o['items']:
                buff += f"\n\t- *{i['i_title']}* x{i['i_count']} - {i['i_sum']} ₽"
            buff += f"\nСумма заказа: {o['sum']} ₽\n"
            all_orders.append(buff)
        return all_orders