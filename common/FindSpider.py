#!/usr/bin/python3
# coding:utf-8

import importlib
import pkgutil
import os
import inspect


class FindSpider(object):
    def __init__(self):
        self.all_spiders = {}
        self.allspiders = []

    def find_modules_names(self, name):
        p = importlib.import_module(name)
        return [name for _, name, _ in pkgutil.iter_importer_modules([os.path.dirname(p.__file__)])]

    def init_spider(self):
        source_list = self.find_modules_names('spiders')
        for source in source_list:
            dict_list = self.find_modules_names('spiders.' + source)
            for dic in dict_list:
                sourceFile = importlib.import_module('spiders.' + source + '.{}'.format(dic))

                for attr in inspect.getmembers(sourceFile):
                    if "Spider" in attr[0] and "Spider" != attr[0]:
                        self.all_spiders[attr[0]] = attr[1]
                        print('找到{}'.format(attr[0]))

        print("所有爬虫已就位，请指示目标!")
        for k, v in self.all_spiders.items():
            self.allspiders.append(k)

        return self.all_spiders, self.allspiders



if __name__ == '__main__':
    a = FindSpider()
    print(a.find_modules_names('common'))
