from datetime import datetime as dt

markdown = "markdown"

messages = {
    "start" : "Hello",
    "categories": "Выберите категорию"
}

# ERRORS
error = {
    "500": "Ошибка 500: `{description}`\n\nОбратитесь к администратору: @{admin}",
    "database": "База данных не отвечает",
    "no_data" : "Нет данных",
}

# 

def get_last_update_format():
    return f"\n{dt.now().strftime('%d %B в %H:%M')}"