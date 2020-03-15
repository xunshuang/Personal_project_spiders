import logging
from abc import ABC, abstractmethod


class Logger():  # 用来记录到控制台的
    def __init__(self):
        logging.basicConfig(format='%(asctime)-15s - %(message)s', level=logging.INFO)

    @staticmethod
    def info(message):
        logging.info(message)


class CallBackLogger():  # 记录到服务器文本的
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filemode='a', filename='log.txt')

    @staticmethod
    def info(message):
        logging.info(message)
