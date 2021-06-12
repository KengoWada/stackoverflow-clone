import json

from tests.base_test import BaseTestCase


class ResetPasswordTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/reset-password/'

    def add_user_return_password_reset_token(self):
        """
        Add a dummy user and return their password reset token
        """
        user = self.create_user(self.user)
        token = self.get_user_password_token(user.email)

        self.set_password_reset_token(user=user, token=token)

        return token

    def test_reset_password(self):
        """
        Test reseting a users password
        """
        token = self.add_user_return_password_reset_token()

        headers = self.get_request_header()
        data = json.dumps({'password': self.other_user['password']})
        url = f'{self.url}{token}'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_reset_password_invalid_password(self):
        """
        Test reseting a users password invalid password
        """
        token = self.add_user_return_password_reset_token()

        headers = self.get_request_header()
        data = json.dumps({'password': ''})
        url = f'{self.url}{token}'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_reset_password_invalid_token(self):
        """
        Test reset password invalid token
        """
        self.add_user_return_password_reset_token()

        headers = self.get_request_header()
        data = json.dumps({'password': 'VeryLongNewPassowrd'})
        url = f'{self.url}some-wrong-text'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_reset_password_twice(self):
        """
        Test reseting a password twice with the same token
        """
        token = self.add_user_return_password_reset_token()

        headers = self.get_request_header()
        data = json.dumps({'password': self.other_user['password']})
        url = f'{self.url}{token}'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)
