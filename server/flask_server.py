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

import pymysql

sys.path.insert(0, '..')
from common.find_spider import FindSpider
from common.my_Logger import Logger
import os
import json
import traceback

spiders_pool = Pool(20)  # 爬虫协程池子20并发

drivers_pool = Pool(2)  # selenium并发池子，自用服务器性能不够，酌情改变此值

task_spiders_queue = Queue()  # 存放消息的队列
task_drivers_queue = Queue()

spiders_dict, spiders = FindSpider().init_spider()  # 初始化爬虫工厂，得到爬虫字典

Logger_2 = Logger()


class SpiderThread(Thread):  # 爬虫线程启动类
    def run(self):
        """
        改写run函数
        :return:
        """
        while True:

            spiders_pool_size = spiders_pool.free_count()  # 目前池子大小
            Logger_2.info(f'目前池子大小------->{spiders_pool_size}')

            while not task_spiders_queue.empty():
                task_queue_size = task_spiders_queue.qsize()  # 任务池的大小
                Logger_2.info(f'任务队列大小------->{task_queue_size}')
                Logger_2.info('-----------------**----------------')


                task = task_spiders_queue.get_nowait()  # 读取任务数据
                Logger_2.info(task)
                Logger_2.info('<-爬虫池收到任务->')
                source = task['source']
                if source in spiders:  # 判断目标爬虫是否存在
                    target = spiders_dict[source]()
                    target.task = task
                    spiders_pool.spawn(target.crawl)
                    print(task)
                else:
                    pass
            time.sleep(3)








if os.path.isfile('../finger/finger.txt'):  # 存放指纹信息的文本文件，懒得用redis，每次启动删除掉finger.txt
    os.remove('../finger/finger.txt')

with open('../finger/finger.txt', 'w') as f:  # 每次启动该服务都会自动重置指纹信息
    f.write('')

# finger_queue = open('finger.txt', 'w')

conn = pymysql.connect(
    host='haha',
    port=10236,
    user='xunshuang',
    passwd='123456',
    db='spider_01_schema',
    charset='utf8'
)  # 全局链接数据库的接口


class User(object):  # 验证用户登录的类

    def __init__(self, username, password, conn):
        self.username = username
        self.password = password
        self.flag = None
        self.conn = conn
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

        self.password = md5(self.password.encode()).hexdigest()

        with self.conn.cursor() as cursor:

            result = cursor.execute(
                'select * from user_passwd where (user_name="%s") and (passwd="%s");' % (self.username, self.password)
            )
            self.conn.commit()


            if result > 0:
                self.flag = True  # 表示执行正确

            else:
                self.flag = False  # 表示执行错误

            if self.flag:
                self.resp = make_response(self.html_1)
                message = md5(f'{self.username + self.password}'.encode())  # 账号与密码存放到cookie
                self.resp.set_cookie('f', self.username)
                self.resp.set_cookie('userinfo', message.hexdigest())

            else:
                try:
                    self.resp.delete_cookie('userinfo')
                except:
                    pass

                self.resp = make_response(self.html_2)
                message = md5(f'{self.username + self.password}'.encode())  # 账号与密码存放到cookie
                self.resp.set_cookie('f', self.username)
                self.resp.set_cookie('userinfo', message.hexdigest())
        time.sleep(1)

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
        # global username
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username, password, conn)
        flag, resp = user.login()
        if flag:
            session['logged_in'] = True

            return resp
        else:
            return resp


@app.route('/crawlinterface', methods=['GET', 'POST'])  # 异步接口
def crawlinterface():

    cookie = request.cookies.get('userinfo')

    f = request.cookies.get('f')
    with conn.cursor() as cursor:
        cursor.execute(
            'select user_name,passwd from user_passwd where user_name="%s";' %(f)
        )
        message = cursor.fetchall()[0]

        conn.commit()

        if md5((f+message[1]).encode()).hexdigest() == cookie:
            check = True
            task = request.json

            task_spiders_queue.put_nowait(task)

            return '任务已收到，立即执行！'
        else:
            check = False


        if not check:
            flash('没有访问权限,重新登录')
            return redirect('/', code=302)



if __name__ == '__main__':
    try:
        spider_thread = SpiderThread()
        spider_thread.start()
        app.run(host='127.0.0.1',port=5000,debug=True)
    except:
        print(traceback.format_exc())
