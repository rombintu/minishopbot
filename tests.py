import unittest
from internal.store.shop import Shop, Item, Category, User
from bson import ObjectId

shop = Shop("mongodb://admin:admin@localhost")

class TestMain(unittest.TestCase):

    def test_login(self):
        u = User(username="user1")
        user = shop.login(u)
        user = shop.login(u)
        print(user.username, user.uuid)

    def test_get_data(self):
        shop.refresh_categories()
        shop.refresh_items()
        print(shop.categories, shop.items)

    def test_create_item(self):
        for i in range(1,20):
            shop.item_create(Item(title=f"item{i+1}", category_title=f"cat5", price=100))

    def test_create_category(self):
        for i in range(1,20):
            shop.category_create(Category(title=f"cat{i+1}"))


if __name__ == '__main__':
    unittest.main()