import unittest
from internal.store.shop import Shop, Item, Category, User
from bson import ObjectId
import io
from PIL import Image

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
        # image_data = io.BytesIO()
        # image = Image.open("./images/image.png")
        # image.save(image_data, format="PNG")
        shop.item_create(
            Item(
                title="item_testing2", category_title="cat18", 
                price=250, photo=None, description="testing3\ntesting4"
                )
            )

    def test_create_category(self):
        for i in range(1,20):
            shop.category_create(Category(title=f"cat{i+1}"))


if __name__ == '__main__':
    unittest.main()