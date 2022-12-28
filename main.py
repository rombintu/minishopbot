# local imports
import os
import logging

# external imports
import telebot
from telebot import types
from dotenv import load_dotenv

# internal imports
from internal import content, database, mem
from internal import keyboards as kb

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)
# db = database.Database(os.getenv("DATABASE"))
admin = os.getenv("BOT_ADMIN", "NoName")

def handle_error(err, too, description="unknown error"):
    logging.error(err)
    bot.send_message(
        too, 
        content.error["500"].format(description, admin), 
        parse_mode="markdown"
    )

@bot.message_handler(commands=['start', 'help'])
def handle_message_start(message):
    bot.send_message(
        message.chat.id, 
        content.messages["start"]
    )

@bot.message_handler(commands=['menu'])
def handle_message_menu(message):
    if not mem.menu.categories:
        bot.send_message(message.chat.id, content.error["no_data"])
        return
    bot.send_message(
        message.chat.id, 
        f"🗂 *Категории*" + content.get_last_update_format(), 
        reply_markup=kb.get_keyboard_categories(),
        parse_mode="markdown"
        )

@bot.callback_query_handler(func=lambda c: c.data)
def servers_callback(c: types.CallbackQuery):
    data = c.data.split("_")
    match data:
        # REFRESH
        case ["refresh", "categories"]:
            mem.menu.refresh_categories()
            bot.edit_message_text(f"🗂 *Категории*" + content.get_last_update_format(),
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_categories(), parse_mode="markdown")
        case ["refresh", "items", _]:
            mem.menu.refresh_items()
            _id = int(data[-1])
            category = mem.menu.get_cat_by_id(_id)
            items = mem.menu.get_items_by_category_id(_id)
            bot.edit_message_text(
                f"{category.emoji} *{category.title.title()}*" + content.get_last_update_format(),
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_items(items=items, category_id=category._id), parse_mode="markdown")
        
        # CATEGORIES
        case ["category", _, ">"]:
            start_i = int(data[1])
            if start_i <= 0: start_i = 0
            bot.edit_message_text(f"🗂 *Категории*",
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_categories(start_i=start_i), parse_mode="markdown")
        case ["category", "id", _]:
            _id = int(data[-1])
            category = mem.menu.get_cat_by_id(_id)
            items = mem.menu.get_items_by_category_id(_id)
            bot.edit_message_text(
                f"{category.emoji} *{category.title.title()}*" + content.get_last_update_format(),
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_items(items=items, category_id=category._id), parse_mode="markdown")
        
        # ITEMS
        case ["item", _, _, ">"]:
            start_i = int(data[-2])
            category_id = int(data[-3])
            if start_i <= 0: start_i = 0
            bot.edit_message_reply_markup(
                c.from_user.id, c.message.id, 
                reply_markup=kb.get_keyboard_items(
                    items=mem.menu.get_items_by_category_id(category_id), 
                    category_id=category_id,
                    start_i=start_i))

        # BASKET
        case ["item", "tobasket", _, _]:
            category_id = int(data[-2])
            item_id = int(data[-1])
            item = mem.menu.get_item_by_id(category_id, item_id)
            user = mem.User(uuid=c.from_user.id)
            # TODO
            user.basket.append(item)
            if user not in mem.users: 
                mem.users.append(user)
            return
            
        # case ["item", "id", _]:
        #     bot.edit_message_text(content.get_last_update_format(),
        #         c.from_user.id, c.message.id, 
        #         reply_markup=kb.get_keyboard_items(), parse_mode="markdown")

@bot.message_handler(commands=['basket'])
def handle_message_menu(message):
    user = None
    for u in mem.users:
        if u.uuid == message.chat.id:
            user = u
    if not user:
        user = mem.User(message.chat.id)
        mem.users.append(user)
    basket = user.get_basket()
    if not basket:
        bot.send_message(message.chat.id, "Корзина пуста")
    else:
        bot.send_message(message.chat.id, "\n".join([item.title for item in  basket]))

def main():
    print("Service status: OK")
    bot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()