'''
test csae base class
'''

import time
import unittest
import requests


class ApiServerUnittest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = "http://127.0.0.1:7890"
        # cls.api_server_process = multiprocessing.Process(target=app.run(port=7890))
        # cls.api_server_process.start()
        time.sleep(0.1)
        cls.api_client = requests.Session()

    @classmethod
    def tearDownClass(cls):
        # cls.api_server_process.terminate()
        # cls.httpbin_process.terminate()
        pass
