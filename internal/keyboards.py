from telebot import types
from internal import mem

def get_keyboard_categories(start_i=0):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btn_refresh = types.InlineKeyboardButton(text="🔄", callback_data=f"refresh_categories")
    btn_next_r = types.InlineKeyboardButton(text="➡️", callback_data=f"category_{start_i+5}_>")
    btn_next_l = types.InlineKeyboardButton(text="⬅️", callback_data=f"category_{start_i-5}_>")
    for i in range(start_i, start_i + 5):
        if i == len(mem.menu.categories): break
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{mem.menu.categories[i].title.title()} {mem.menu.categories[i].emoji}", 
                callback_data=f"category_id_{mem.menu.categories[i]._id}"))

    if start_i == 0 and start_i + 5 >= len(mem.menu.categories):
        keyboard.add(btn_refresh)
    elif start_i + 5 >= len(mem.menu.categories): 
        keyboard.add(btn_next_l, btn_refresh)
    elif start_i == 0: 
        keyboard.add(btn_refresh, btn_next_r)
    else: 
        keyboard.add(btn_next_l, btn_refresh, btn_next_r,)
    return keyboard

def get_keyboard_items(items, category_id, start_i=0):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    btn_refresh = types.InlineKeyboardButton(text="🔄", callback_data=f"refresh_items_{category_id}")
    btn_next_r = types.InlineKeyboardButton(text="➡️", callback_data=f"item_{category_id}_{start_i+10}_>")
    btn_next_l = types.InlineKeyboardButton(text="⬅️", callback_data=f"item_{category_id}_{start_i-10}_>")
    btn_back_to_menu = types.InlineKeyboardButton(text="↩️", callback_data=f"category_{0}_>")
    for i in range(start_i, start_i + 10):
        if i == len(items): break
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{items[i].title} ...", 
                callback_data=f"item_id_{category_id}_{items[i]._id}"),
            types.InlineKeyboardButton(
                text=f"{items[i].price:,} ₽ 🛒", 
                callback_data=f"item_tobasket_{category_id}_{items[i]._id}")
            )

    if start_i == 0 and start_i + 10 >= len(items):
        keyboard.add(btn_refresh)
    elif start_i + 10 >= len(items): 
        keyboard.add(btn_next_l, btn_refresh)
    elif start_i == 0: 
        keyboard.add(btn_refresh, btn_next_r)
    else: 
        keyboard.add(btn_next_l, btn_refresh, btn_next_r)
    keyboard.add(btn_back_to_menu)
    return keyboard