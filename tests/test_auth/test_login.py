import json

from tests.base_test import BaseTestCase


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/login'

    def register_user(self):
        """
        Create a dummy user
        """
        response = self.test_client.post(
            '/auth/register', content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        """
        Test logging in a valid user
        """
        self.register_user()
        response = self.test_client.post(
            self.url, content_type='application/json', data=json.dumps(self.user))
        # print(json.loads(response.data.decode()))
        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials(self):
        """
        Test logging in with invalid credentials
        """
        self.register_user()
        response = self.test_client.post(
            self.url, content_type='application/json', data=json.dumps(self.invalid_user))
        self.assertEqual(response.status_code, 400)
