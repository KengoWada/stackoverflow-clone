import json

from tests.base_test import BaseTestCase


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/login'

    def test_login(self):
        """
        Test logging in a valid user
        """
        self.create_user(self.user)

        headers = self.get_request_header()
        data = json.dumps(self.user_login)

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        """
        Test logging in with invalid credentials
        """
        self.create_user(self.user)

        headers = self.get_request_header()
        data = json.dumps(self.invalid_user)

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    # TODO: Implement login field validation
    # def test_login_invalid_request(self):
    #     self.create_user(self.user)

    #     headers = self.get_request_header()
    #     data = json.dumps({})

    #     response = self.test_client.post(self.url, headers=headers, data=data)

    #     self.assertEqual(response.status_code, 400)
