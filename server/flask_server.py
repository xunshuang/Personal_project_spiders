#!/usr/bin/python3
# coding:utf-8
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import Queue
from gevent import spawn
import time
from threading import Thread
from flask import Flask, request, render_template, redirect, flash, session, make_response
from hashlib import md5
import sys

sys.path.insert(0, '..')
from common.find_spider import FindSpider
from common.my_Logger import Logger
import os
import json
import traceback

spiders_pool = Pool(20)  # 爬虫池子20并发

drivers_pool = Pool(2)  # selenium并发池子，自用服务器性能不够，酌情改变此值

task_spiders_queue = Queue(50)  # 存放消息的队列
task_drivers_queue = Queue(50)

spiders_dict, spiders = FindSpider().init_spider()  # 初始化爬虫工厂，得到爬虫字典

Logger_2 = Logger()


class SpiderPool(Thread):  # 爬虫线程启动类
    def run(self):
        """
        改写run函数
        :return:
        """
        while True:
            spiders_pool_size = spiders_pool.free_count()  # 池子大小
            Logger_2.info(f'爬虫池总大小------->{spiders_pool_size}')
            spiders_pool_size = spiders_pool.free_count()  # 目前池子大小
            Logger_2.info(f'目前池子大小为------->{spiders_pool_size}')

            task_queue_size = task_spiders_queue.qsize()  # 任务池的大小
            Logger_2.info(f'任务队列大小------->{task_queue_size}')
            try:
                task = task_spiders_queue.get_nowait()  # 读取任务数据
                Logger_2.info('<-爬虫池收到任务->')
                source = task['source']
                if source in spiders:  # 判断目标爬虫是否存在
                    target = spiders_dict[source]()
                    target.task = task
                    spiders_pool.spawn(target.crawl)
            except:
                pass
            time.sleep(3)


spider_pool = SpiderPool()
spider_pool.start()

if os.path.isfile('../finger/finger.txt'):  # 存放指纹信息的文本文件，懒得用redis，每次启动删除掉finger.txt
    os.remove('../finger/finger.txt')

with open('../finger/finger.txt', 'w') as f:  # 每次启动该服务都会自动重置指纹信息
    f.write('')


# finger_queue = open('finger.txt', 'w')


class User(object):  # 验证用户登录的类

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.flag = None
        self.html_1 = '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录成功</title>
    <style>
        .index {
            text-align: center;
            background: darkgreen;
        }

        .down {
            text-align: center;
        }
    </style>
    <script>
        function f() {
            window.location.href('/check')
        }
    </script>
</head>
<body>

<div class="index">
    <h2><strong>登录成功</strong></h2>
</div>
<div class="down">
    <p>闲在家里无事做，写个网站来娱乐-----孟帅</p>
</div>

</body>
</html>
'''
        self.html_2 = '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录失败</title>
    <style>
        .index {
            text-align: center;
            background: darkgreen;
        }

        .down {
            text-align: center;
        }
    </style>
    <script>
        function f() {
            window.location.href('/check')
        }
    </script>
</head>
<body>

<div class="index">
    <h2><strong>登录失败</strong></h2>
</div>
<div class="down">
    <p>闲在家里无事做，写个网站来娱乐-----孟帅</p>
</div>

</body>
</html>
'''
        self.resp = ''  # 好low啊！哈哈哈哈不会弄。

        with open('userinfo.txt', 'r') as f:
            users_list = f.readlines()
            for i in users_list:
                i = json.loads(i)
                if self.username == i['username']:
                    if self.password == i['password']:
                        self.flag = True
                        if self.flag:
                            print('deng lu cg')
                            message = md5(f'{i["username"] + i["password"]}'.encode())  # 账号与密码存放到cookie
                            self.resp = make_response(self.html_1)
                            self.resp.set_cookie('user', message.hexdigest())
                    else:
                        self.flag = False
                        try:
                            self.resp.delete_cookie('user')
                        except:
                            pass
                        self.resp = make_response(self.html_2)
                        message = md5(f'{self.username + self.password}'.encode())
                        self.resp.set_cookie('user', message.hexdigest())
                else:
                    continue

    def login(self):

        return self.flag, self.resp


app = Flask(__name__, template_folder='../templates')
app.secret_key = 'adminxyz123..!&'
app.config['SESSION_COOKIE_NAME'] = 'SessionAliveFinger'


@app.route('/', methods=['GET', 'POST'])
def login_index():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        global username
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username, password)
        flag, resp = user.login()
        if flag:
            session['logged_in'] = True

            return resp
        else:
            return resp


@app.route('/crawlinterface', methods=['GET', 'POST'])  # 异步接口
def crawlinterface():
    cookie = request.cookies.get('user')
    with open('userinfo.txt', 'r') as f:
        u = f.readlines()
    check = False
    for i in u:
        if cookie == md5((json.loads(i)['username'] + json.loads(i)['password']).encode()).hexdigest():
            task = request.json
            task_spiders_queue.put_nowait(task)
            check = True
            return '请求已收到'
        else:
            check = False
    if not check:
        flash('没有访问权限,重新登录')
        return redirect('/', code=302)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except:
        print(traceback.format_exc())
