from telebot import types
from internal import mem

categories_on_page = 5
items_on_page = 6

def get_keyboard_categories(start_i=0):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btn_refresh = types.InlineKeyboardButton(text="🔄", callback_data=f"refresh_categories")
    btn_next_r = types.InlineKeyboardButton(text="➡️", callback_data=f"category_{start_i+categories_on_page}_>")
    btn_next_l = types.InlineKeyboardButton(text="⬅️", callback_data=f"category_{start_i-categories_on_page}_>")
    for i in range(start_i, start_i + categories_on_page):
        if i == len(mem.menu.categories): break
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{mem.menu.categories[i].title.title()} {mem.menu.categories[i].emoji}", 
                callback_data=f"category_id_{mem.menu.categories[i]._id}"))

    if start_i == 0 and start_i + categories_on_page >= len(mem.menu.categories):
        keyboard.add(btn_refresh)
    elif start_i + categories_on_page >= len(mem.menu.categories): 
        keyboard.add(btn_next_l, btn_refresh)
    elif start_i == 0: 
        keyboard.add(btn_refresh, btn_next_r)
    else: 
        keyboard.add(btn_next_l, btn_refresh, btn_next_r,)
    return keyboard

def get_keyboard_items(items, category_id, start_i=0):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btn_refresh = types.InlineKeyboardButton(text="🔄", callback_data=f"refresh_items_{category_id}")
    btn_next_r = types.InlineKeyboardButton(text="➡️", callback_data=f"item_{category_id}_{start_i+items_on_page}_>")
    btn_next_l = types.InlineKeyboardButton(text="⬅️", callback_data=f"item_{category_id}_{start_i-items_on_page}_>")
    btn_back_to_menu = types.InlineKeyboardButton(text="↩️", callback_data=f"category_{0}_>")
    for i in range(start_i, start_i + items_on_page):
        if i == len(items): break
        keyboard.add(
            types.InlineKeyboardButton(
                # text=f"{items[i].title}", 
                 text=f"{items[i].title}", 
                callback_data=f"item_id_{category_id}_{items[i]._id}"),
            types.InlineKeyboardButton(
                text=f"{items[i].capacity} 📦 {items[i].price:,} ₽", 
                callback_data=f"item_tobasket_{category_id}_{items[i]._id}")
            )

    if start_i == 0 and start_i + items_on_page >= len(items):
        keyboard.add(btn_refresh)
    elif start_i + items_on_page >= len(items): 
        keyboard.add(btn_next_l, btn_refresh)
    elif start_i == 0: 
        keyboard.add(btn_refresh, btn_next_r)
    else: 
        keyboard.add(btn_next_l, btn_refresh, btn_next_r)
    keyboard.add(btn_back_to_menu)
    return keyboard

def get_keyboard_basket(basket, start_i=0):
    keyboard = types.InlineKeyboardMarkup()
    btn_refresh = types.InlineKeyboardButton(text="🔄", callback_data="refresh_basket")
    btn_create_order = types.InlineKeyboardButton(text="Оформить 📩", callback_data=f"basket_order_create_{basket.user_id}")
    items = basket.get_items()
    if not items:
        keyboard.add(btn_refresh)
        return keyboard
    btn_next_r = types.InlineKeyboardButton(text="➡️", callback_data=f"basket_{start_i+items_on_page}_>")
    btn_next_l = types.InlineKeyboardButton(text="⬅️", callback_data=f"basket_{start_i-items_on_page}_>")
    for i in range(start_i, start_i + items_on_page):
        if i == len(basket.items): break
        keyboard.add(
            types.InlineKeyboardButton( 
                 text=f"{items[i].title}", 
                callback_data=f"basket_{items[i]._id}"),
            types.InlineKeyboardButton(
                text=f"{items[i].capacity} 📦 {items[i].price:,} ₽", 
                callback_data=f"basket_{items[i]._id}")
            )

    if start_i == 0 and start_i + items_on_page >= len(items):
        keyboard.add(btn_create_order, btn_refresh)
    elif start_i + items_on_page >= len(items): 
        keyboard.add(btn_next_l, btn_refresh)
        keyboard.add(btn_create_order)
    elif start_i == 0: 
        keyboard.add(btn_refresh, btn_next_r)
        keyboard.add(btn_create_order)
    else: 
        keyboard.add(btn_next_l, btn_refresh, btn_next_r)
        keyboard.add(btn_create_order)
    return keyboard