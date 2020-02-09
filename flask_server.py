# coding:utf-8

from flask import Flask, jsonify, request, render_template
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
app = Flask(__name__, template_folder='templates')


@app.route('/virus', methods=["POST"])
def virus():
    try:
        task = request.json
    except:
        print("data type error")
        return jsonify({"message": "失败", "reason": "数据类型错误"})

    try:
        city = task['city']
        spider = task['spider']
        flag = True
    except:
        spider = request.form.get("spider")
        city = request.form.get("city")
        flag = False


    if spider not in spiders:
        if flag:
            return jsonify({"message": "失败", "reason": "未找到爬虫文件"})
        else:
            return str("message: 失败, reason: 未找到爬虫文件")

    spider = spiders[spider]()
    try:
        result = spider.parse_result(city)
        if flag:
            return jsonify({"message": "成功", "result": "{}".format(result.decode())})
        else:
            return str(result).replace('{','').replace('}','').replace("'",'')
    except:
        print(traceback.format_exc())


@app.route('/', methods=["GET","POST"])
def index_get():
    if request.method == 'GET':
        return render_template(template_name_or_list='index.html')
    else:
        return '请求方式错误'


# @app.route('/web/post_form.js',methods=["POST"])
# def post_form():


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
