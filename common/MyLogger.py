import logging


class Logger:
    def __init__(self):
        logging.basicConfig(format='%(asctime)-15s - %(message)s', level=logging.INFO)

    @staticmethod
    def info(message):
        logging.info(message)