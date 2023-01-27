import logging

def new_logger():
    return logging.Logger(name="logger", level=logging.DEBUG)