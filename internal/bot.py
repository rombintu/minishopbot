# local imports
import os

# external imports
import telebot
from telebot import types
from dotenv import load_dotenv

# internal imports
from internal import content
from internal import keyboards as kb
from internal.logger import new_logger
from internal.store.shop import Shop, User
from bson import ObjectId

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)
shop = Shop(os.getenv("DATABASE"))
log = new_logger()

@bot.message_handler(commands=['shop', 'start'])
def handle_message_shop(m):
    if not shop.categories:
        bot.send_message(m.chat.id, content.error["no_data"])
        return
    bot.send_message(
        m.chat.id, 
        f"🗂 *Категории*" + content.get_last_update_format(), 
        reply_markup=kb.get_keyboard_categories(shop.get_categories()),
        parse_mode=content.markdown
        )
    user = shop.login(User(m.chat.id, m.from_user.first_name))
    basket = user.get_basket()
    bot.send_message(
        m.chat.id, basket.get_content(),
        parse_mode=content.markdown, 
        reply_markup=kb.get_keyboard_basket(basket)
    )

# TODO
@bot.message_handler(commands=['basket'])
def handle_message_basket(m):
    user = shop.login(User(m.chat.id, m.from_user.first_name))
    basket = user.get_basket()
    bot.send_message(
        m.chat.id, basket.get_content(),
        parse_mode=content.markdown, 
        reply_markup=kb.get_keyboard_basket(basket)
    )

@bot.message_handler(commands=['orders'])
def handle_message_order(m):
    orders = shop.get_orders_info(m.chat.id)
    if not orders:
        bot.send_message(
            m.chat.id, "Заказы не найдены, посетите магазин /shop",
            parse_mode=content.markdown, 
            reply_markup=kb.get_keyboard_hide_item()
        )
        return
    for order in orders:
        bot.send_message(
            m.chat.id, order,
            parse_mode=content.markdown, 
            reply_markup=kb.get_keyboard_hide_item()
        )


@bot.callback_query_handler(func=lambda c: c.data)
def servers_callback(c: types.CallbackQuery):
    data = c.data.split("_")
    match data:
        # REFRESH
        case ["refresh", "categories"]:
            shop.refresh_categories()
            bot.edit_message_text(f"🗂 *Категории*" + content.get_last_update_format(),
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_categories(
                    shop.get_categories()), parse_mode=content.markdown)
        case ["refresh", "items", _]:
            shop.refresh_items()
            _id = data[-1]
            category = shop.get_cat_by_id(_id)
            if not category:
                bot.send_message(c.message.chat.id, "Данной категории больше не существует, обновите список")
                return
            items = shop.get_items_by_category_id(category.title)
            bot.edit_message_text(
                f"{category.emoji} *{category.title.title()}*" + content.get_last_update_format(),
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_items(
                    items=items, category_id=category._id), parse_mode=content.markdown)
        case ["refresh", "basket"]:
            user = shop.login(User(c.message.chat.id))
            basket = user.get_basket()
            bot.edit_message_text(
                basket.get_content(), c.message.chat.id, c.message.id,
                reply_markup=kb.get_keyboard_basket(basket)
            )
        case ["basket", _, ">"]:
            start_i = int(data[1])
            if start_i <= 0: start_i = 0
            user = shop.login(User(c.message.chat.id))
            basket = user.get_basket()
            bot.edit_message_text(
                basket.get_content(), c.message.chat.id, c.message.id,
                reply_markup=kb.get_keyboard_basket(basket, start_i=start_i)
            )
        # CATEGORIES
        case ["category", _, ">"]:
            start_i = int(data[1])
            if start_i <= 0: start_i = 0
            bot.edit_message_text(f"🗂 *Категории*",
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_categories(
                    shop.get_categories(), start_i=start_i), parse_mode=content.markdown)

        case ["category", "id", _]:
            category_id = data[-1]
            category = shop.get_cat_by_id(category_id)
            if not category:
                bot.send_message(c.message.chat.id, "Данной категории больше не существует, обновите список")
                return 
            items = shop.get_items_by_category_id(category.title)
            bot.edit_message_text(
                f"{category.emoji} *{category.title.title()}*" + content.get_last_update_format(),
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_items(
                    items=items, category_id=category._id), parse_mode=content.markdown)
        
        # ITEMS
        case ["item", _, _, ">"]:
            start_i = int(data[-2])
            category_id = data[-3]
            category = shop.get_cat_by_id(category_id)
            if not category:
                bot.send_message(c.message.chat.id, "Данной категории больше не существует, обновите список")
                return
            if start_i <= 0: start_i = 0
            bot.edit_message_reply_markup(
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_items(
                    items=shop.get_items_by_category_id(category.title), 
                    category_id=category_id,
                    start_i=start_i))

        # BASKET
        case ["item", "tobasket", _, _]:
            category_id = data[-2]
            item_id = data[-1]
            category = shop.get_cat_by_id(category_id)
            if not category:
                bot.send_message(c.message.chat.id, "Данной категории больше не существует, обновите список")
                return
            item = shop.get_item_by_id(category.title, item_id)
            if not item:
                bot.send_message(c.message.chat.id, "Данного товара больше не существует, обновите список")
                return
            user = shop.login(User(c.from_user.id))
            # TODO
            user.to_basket(item)
            # bot.send_message(c.message.chat.id, f"/basket 🛒 + {item.capacity} *{item.title}*", parse_mode=content.markdown)
        
        case ["basket", "clear"]:
            user = shop.login(User(c.message.chat.id))
            user.basket.clear()
            bot.edit_message_text(
                user.get_basket().get_content(), c.message.chat.id, c.message.id,
                reply_markup=kb.get_keyboard_basket(user.get_basket())
            )
        case ["basket", "remove", _]:
            item_id = data[-1]
            user = shop.login(User(c.message.chat.id))
            user.basket.remove(item_id)
            bot.edit_message_text(
                user.get_basket().get_content(), c.message.chat.id, c.message.id,
                reply_markup=kb.get_keyboard_basket(user.get_basket())
            )
        case ["item", "id", _]:
            item_id = data[-1]
            item = shop.store.items.find_one({"_id": ObjectId(item_id)})
            keyboard = kb.get_keyboard_hide_item()
            if not item:
                bot.send_message(c.message.chat.id, "Товар был изменен или удален, обновите каталог")
                return
            elif not item["photo"]:
                bot.send_message(c.message.chat.id, item["description"], reply_markup=keyboard)
                return
            bot.send_photo(c.message.chat.id, item["photo"], caption=item["description"], reply_markup=keyboard)
        case ["item", "hide"]:
            bot.delete_message(c.message.chat.id, c.message.id, timeout=1)
        case ["basket", "order", "create"]:
            user = shop.login(User(c.message.chat.id))
            order = user.create_order()
            mess = "Корзина пуста, обновите информацию"
            if order:
                mess = "Заявка на оформление отправлена /orders"
                shop.store.orders.insert_one(order.__dict__)
            bot.send_message(c.message.chat.id, mess)
    return