import requests
from fake_useragent import UserAgent
from collections import Iterator
from abc import ABC, abstractmethod

'''
-------------------------------------------------------------------------------------------------------------------------------------------------------
|                                      
|        # 维持会话功能                 
|        # log记录功能                
|        # 爬虫队列功能                   
|        # SSL忽略功能                  
|        # 反馈错误功能                  
|        # 替换请求头功能                 
|        # 替换IP功能                   
|        # 重试功能                      
|                                      
|    coder:Xunshuang                    
|    date:2020/01/14                    
-------------------------------------------------------------------------------------------------------------------------------------------------------
'''


class Spider(ABC):
    def __init__(self):

        self.retry = 3
        self.timeout = 15
        self.allow_redirects = True
        self.Sess = None
        self.allow_status_code = [200, 301, 302]
        self.meta = {}
        self.result = []  # 最后爬取处理的结果

    def __create_new_session__(self, new_session=False, UA=False, cookie=None):
        if not self.Sess or new_session:  # 如果没有初始化session，或者是new_session=True，就新建一个会话
            self.Sess = requests.Session()
            self.Sess.verify = False  # 直接取消SSL认证

        if UA:
            self.Sess.headers.update({'User-Agent': f'{UserAgent().random}'})

        if cookie:
            if isinstance(cookie, dict):
                self.Sess.cookies.update({'cookie': cookie})
            else:
                raise Exception('cookie 不是一个字典格式')
        return self.Sess

    def process_result(self, resp):  # 处理resp的
        if not isinstance(resp, Iterator):
            if resp:
                self.result.append(resp)
                return

        for i in resp:
            if isinstance(i, Iterator):
                self.process_result(i)

            else:
                if i:
                    self.result.append(i)

    def check_status(self, resp):
        resp.status_code = 200  # 将响应状态码强行改为200
        return resp

    def do_nothing(self, resp):
        return resp  # 什么也不做，这一步主要为了获取cookie

    def set_proxy(self):
        proxy = self.get_proxy()
        proxy = {
            'http': 'http://127.0.0.1:8889',  # 默认走fiddler
            'https': 'https://127.0.0.1:8889'
        }
        return proxy

    def get_proxy(self):
        # 日后链接IP池用，先保留
        return ''

    def request(self, method='GET', next_function=None, proxy=None, new_session=False, meta=None, UA=False, cookie=None,
                retry=None, response_check=None, *args, **kwargs):
        """
        :param method: 请求方式
        :param next_function: 解析函数
        :param proxy: 代理，默认没有代理
        :param new_session: 是否维持会话
        :param meta: 传递参数
        :param UA: User-Agent，True时自动替换UA
        :param cookie: 如果有值则替换header里的cookie
        :param retry: 重试次数，为空时自动重试三次
        :param response_check:检查响应错误
        :param kwargs:获取url等参数
        :return:
        """
        if not next_function:
            # 没有新的解析函数 直接报错
            raise Exception('The next_function is None')

        self.Sess = self.__create_new_session__(new_session=new_session, UA=UA, cookie=cookie)  # 根据规则是否创建会话

        try:
            url = kwargs.pop('url')
        except:
            raise Exception('url 错误或者没有传参数')

        try:
            allow_redirects = kwargs.pop('allow_redirects')

        except:
            allow_redirects = self.allow_redirects  # 默认允许重定向

        headers = kwargs.get('headers')  # 获取headers
        if headers:  # 如果有headers，且UA为True，将headers里的UA删掉
            if UA:
                try:
                    headers.pop('User-Agent')
                except:
                    try:
                        headers.pop('user-agent')
                    except:
                        pass

        if retry == False:  # 不允许重试
            retry = 0
        elif not retry:  # retry = None
            retry = self.retry  # 为None时，默认重试次数3
        else:
            retry = int(retry)  # 兼容字符串

        # ----以下留给代理池功能 ，暂时只写127.0.0.1走fiddler或者自由派----

        # ----------------------------------------------------------

        if not meta:  # 如果没有meta的值，略过
            pass
        elif isinstance(meta, dict):  # 如果有meta的值，判断是否为dict，是的话，将self.meta替换为meta,做全局记录
            self.meta = meta

        while retry:
            if proxy == 'USE':  # USE表示使用代理
                proxy = self.set_proxy()
                response = self.Sess.request(url=url, method=method, proxies=proxy, allow_redirects=allow_redirects)
                if response_check:
                    response = response_check(response)
                if response.status_code not in self.allow_status_code:
                    raise Exception(f'代理失败，或者其他原因，状态码:{response.status_code}')
                else:
                    break  # 保留功能
                retry -= 1

            else:  # 其余情况一律不使用代理
                response = self.Sess.request(url=url, method=method, allow_redirects=allow_redirects)
                if response_check:
                    response = response_check(response)
                if response.status_code not in self.allow_status_code:
                    raise Exception(f'请求失败,状态码:{response.status_code}')
                else:
                    break
                retry -= 1

        if not response:  # 如果没有响应
            raise Exception('没有获得响应，请尝试检查url')

        else:
            resp = next_function({'req': self.Sess}, response)
            return resp

    @abstractmethod
    def start_request(self):
        pass

    def crawl(self):
        if not isinstance(self.start_request(), Iterator):
            raise Exception('start_request不是一个生成器')

        try:
            for i in self.start_request():  # 循环执行start_request
                self.process_result(i)

        except Exception as e:
            print(e)
