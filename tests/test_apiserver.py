'''
test cases

'''
import unittest
from tests.base import ApiServerUnittest


class TestApiServer(ApiServerUnittest):
    def setUp(self):
        super(TestApiServer, self).setUp()
        # self.clear_users()

    def tearDown(self):
        super(TestApiServer, self).tearDown()


    def create_user(self, uid, name, password):
        url = "%s/api/users/%d" %(self.host, uid)
        data = {
            'name': name,
            'password': password
        }
        return self.api_client.post(url, json=data)

    def test_create_user_not_existed(self):
        # self.clear_users()

        url = "%s/api/users/%d" % (self.host, 1000)
        data = {
            "name": "user1",
            "password": "123456"
        }
        resp = self.api_client.post(url, json=data)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(True, resp.json()["success"])

    def test_create_user_existed(self):
        resp = self.create_user(1000, 'user1', '123456')
        resp = self.create_user(1000, 'user1', '123456')
        self.assertEqual(500, resp.status_code)

if __name__ == '__main__':
    unittest.main()