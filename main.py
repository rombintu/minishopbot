from internal.bot import bot

def main():
    print("Service status: OK")
    bot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()