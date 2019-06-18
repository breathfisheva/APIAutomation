
import requests
import unittest
from requests.sessions import Session
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  #for python3, already put ulrparse to urllib.parse
import HTMLTestRunner


class DemoApi(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = Session() #登录接口的http响应会把session以 cookie的形式set到客户端，之后的接口都会使用此session去请求

    def login(self, username, password):
        url = urljoin(self.base_url, 'login')
        data = {
            'username': username,
            'password': password
        }

        response = self.session.post(url, data=data).json()
        return response

    def info(self):
        url = urljoin(self.base_url, 'info')
        response = self.session.get(url).json()
        return response


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls): #在测试之前准备的环境
        cls.base_url = 'http://127.0.0.1:7890'
        cls.username = 'admin'
        cls.password = '1234567'
        cls.app = DemoApi(cls.base_url)

    def test_login(self):
        response = self.app.login(self.username, self.password)
        assert response['code'] == 200
        assert response['msg'] == 'success'

    def test_info(self):
        self.app.login(self.username, self.password) #先登录接口的http响应会把session以 cookie的形式set到客户端，之后的接口都会使用此session去请求
        response = self.app.info()
        assert response['code'] == 200
        assert response['msg'] == 'success'
        assert response['data'] == 'info'


suite = unittest.TestSuite()

#1.找到所有的testcase， unittest的框架的test case要以test开头
# all_cases = unittest.defaultTestLoader.discover('.', 'test_*.py')
# for case in all_cases:
#     suite.addTest(case)

# 2.add 1 test case
suite.addTest(TestLogin('test_login'))
suite.addTest(TestLogin('test_info'))

with open('HTMLReport.html', 'wb') as f:
    runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='test report', description='generate use HTMLTestRunner', verbosity=2)
    runner.run(suite)



