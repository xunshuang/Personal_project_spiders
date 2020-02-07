# coding:utf-8

from flask import Flask, jsonify, request
import os
import json
import importlib
import pkgutil
import inspect
import traceback
import sys


def find_module_names(name):
    p = importlib.import_module(name)
    return [name for _, name, _ in pkgutil.iter_modules([os.path.dirname(p.__file__)])]


def init_spider():
    all_spiders = {}
    source_list = find_module_names('spiders')
    for source in source_list:
        sourceFile = importlib.import_module('spiders.{}'.format(source))

        for attr in inspect.getmembers(sourceFile):
            if "Spider" in attr[0]:
                all_spiders[attr[0]] = attr[1]
                print('找到{}'.format(attr[0]))
    return all_spiders


spiders = init_spider()
app = Flask(__name__)


@app.route('/virus', methods=["POST"])
def virus():
    try:
        task = request.json
    except:
        print("data type error")
        return jsonify({"message": "error", "reason": "data type error"})

    city = task['city']
    spider = task['spider']
    if spider not in spiders:
        return jsonify({"message": "error", "reason": "spiderfile not found"})
    print('{} is working'.format(spider))
    spider = spiders[spider]()
    try:
        result = spider.parse_result(city)
        return jsonify({"message": "sess", "result": "{}".format(result)})
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
