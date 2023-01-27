from internal.bot import bot, log
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    log.debug("Service is starting...")
    bot.polling(none_stop=True, timeout=60)

if __name__ == "__main__":
    main()