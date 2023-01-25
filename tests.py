import unittest
from internal.store.database import Shop, Item, Category

shop = Shop("mongodb://admin:admin@localhost")

class TestMain(unittest.TestCase):

    def test_login(self):
        user = shop.login(0, "user")
        user = shop.login(0, "user")
        print(user.username, user.uuid)

    def test_get_data(self):
        shop.refresh_categories()
        shop.refresh_items()
        print(shop.categories, shop.items)

    def test_create_item(self):
        item1 = Item("item1", 0, 100)
        item2 = Item("item2", 1, 200, "400ml")
        item3 = Item("item3", 1, 300)
        
        shop.item_create(item1)
        shop.item_create(item1)
        shop.item_create(item2)
        shop.item_create(item3)


if __name__ == '__main__':
    unittest.main()