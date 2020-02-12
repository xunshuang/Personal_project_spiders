# coding:utf-8

from flask import Flask, jsonify, request, render_template, redirect
from requests import Session
from common.find_spider import FindSpider
import os
import json
import importlib
import pkgutil
import inspect
import traceback
import sys

spiders_dict, spiders = FindSpider().init_spider()
app = Flask(__name__, template_folder='templates')



@app.route('/', methods=["GET", "POST"])  # 主页
def index_get():
    global Sess
    Sess = Session()
    return render_template(template_name_or_list='index.html')


@app.route('/virus_index', methods=['GET'])  # 冠状病毒主页
def virus_search():
    return render_template(template_name_or_list='virus_html/virus.html')


@app.route('/virusSpider', methods=["POST"])  # 冠状病毒搜索器
def virus():
    try:
        task = request.json
    except:
        print("data type error")
        return jsonify({"message": "失败", "reason": "数据类型错误"})

    try:
        city = task['city']
        flag = True
    except:

        city = request.form.get("city")
        flag = False

    spider = 'VirusSpider'
    print("city:{}".format(city))
    if spider not in spiders:
        if flag:
            return jsonify({"message": "失败", "reason": "未找到爬虫文件"})
        else:
            return str("message: 失败, reason: 未找到爬虫文件")

    spider = spiders_dict[spider]()
    try:
        result = spider.parse_result(city)
        if flag:

            return jsonify({"message": "成功", "result": "{}".format(result.decode())})
        else:
            return str(result).replace('{', '').replace('}', '').replace("'", '')
    except:
        print(traceback.format_exc())


@app.route('/novels_index', methods=['GET'])  # 小说阅读主页
def novel_search():
    return render_template(template_name_or_list='novels_html/novel_search.html')


@app.route('/NovelListSpider', methods=['POST'])  # 小说列表页展示
def novel_name_search():
    try:
        task = request.json
    except:
        print("data type error")
        return jsonify({"message": "失败", "reason": "数据类型错误"})

    try:
        novel_name = task['novel_name']
    except:
        novel_name = request.form.get("novel_name")

    spider = 'NovelListSpider'
    print("novel name:{}".format(novel_name))
    if spider not in spiders:
        return jsonify({"message": "失败", "reason": "未找到爬虫文件"})

    spider = spiders_dict[spider]()
    try:
        global Sess  # 维持小说爬虫会话

        novels_name, novels_writer, novels_sub, novels_id, Sess = spider.main(keyword=novel_name)  # 列表页数据

        return render_template(template_name_or_list='novels_html/novel_list_result.html', novels_name=novels_name,
                               novels_writer=novels_writer, novels_sub=novels_sub, novels_id=novels_id, chapter='')
    except:
        print(traceback.format_exc())


@app.route('/NovelChapterSpider', methods=['GET'])  # 小说章节页展示
def novel_chapter_search():
    novel_id = request.args.get('novel_id', type=str)
    spider = 'NovelChapterSpider'
    print("novel id:{}".format(novel_id))
    if spider not in spiders:
        return jsonify({"message": "失败", "reason": "未找到爬虫文件"})
    spider = spiders_dict[spider]()
    global Sess  # 维持小说爬虫会话
    chapter, Sess, hrefs = spider.main(Sess=Sess, novel_id=novel_id)
    return render_template('novels_html/novel_chapter.html', chapter=chapter, href=hrefs)



@app.route('/NovelContentSpider', methods=['GET'])  # 小说正文页
def novel_content_search():
    content_id = request.args.get('content_id', type=str)
    spider = 'NovelContentSpider'
    print("content id:{}".format(content_id))
    if spider not in spiders:
        return jsonify({"message": "失败", "reason": "未找到爬虫文件"})
    spider = spiders_dict[spider]()
    try:
        global Sess
        text = spider.main(Sess=Sess, content_id=content_id)
        return render_template('novels_html/novel_content.html', text=text)
    except:
        print(traceback.format_exc())


# @app.route('/web/post_form.js',methods=["POST"])
# def post_form():


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
