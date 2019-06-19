from yamltestcase.send_request import *
from yamltestcase.loader import load_yaml_file
import unittest

class TestApiServer(unittest.TestCase):

    def test_create_user_not_existed(self):
        # # self.clear_users()
        #
        # url = "%s/api/users/%d" % (self.host, 1000)
        # data = {
        #     "name": "user1",
        #     "password": "123456"
        # }
        # resp = self.api_client.post(url, json=data)
        #
        # self.assertEqual(201, resp.status_code)
        # self.assertEqual(True, resp.json()["success"])

        testcases = load_yaml_file('data.yml')
        run_single_testcase(testcases[0]['test'])

if __name__ == '__main__':
    unittest.main()