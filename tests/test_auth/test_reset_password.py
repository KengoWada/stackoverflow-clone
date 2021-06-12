import json

from tests.base_test import BaseTestCase
from api.utils import get_token


class ResetPasswordTestCase(BaseTestCase):

    def test_reset_password(self):
        """
        Test reseting a users password
        """
        user = self.create_user(self.user)
        token = get_token(user.email)
        self.set_password_reset_token(user=user, token=token)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'password': self.other_user['password']})
        url = f'/auth/reset-password/{token}'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_reset_password_invalid_password(self):
        """
        Test reseting a users password invalid password
        """
        user = self.create_user(self.user)
        token = get_token(user.email)
        self.set_password_reset_token(user=user, token=token)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'password': ''})
        url = f'/auth/reset-password/{token}'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_reset_password_invalid_token(self):
        """
        Test reset password invalid token
        """
        user = self.create_user(self.user)
        token = get_token(user.email)
        self.set_password_reset_token(user=user, token=token)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'password': 'VeryLongNewPassowrd'})
        url = f'/auth/reset-password/some-wrong-text'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_reset_password_twice(self):
        """
        Test reseting a password twice with the same token
        """
        user = self.create_user(self.user)
        token = get_token(user.email)
        self.set_password_reset_token(user=user, token=token)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'password': self.other_user['password']})
        url = f'/auth/reset-password/{token}'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)
