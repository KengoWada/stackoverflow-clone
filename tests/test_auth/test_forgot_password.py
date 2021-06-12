import json

from tests.base_test import BaseTestCase


class ForgotPasswordTestCase(BaseTestCase):

    def test_forgot_password(self):
        """
        Test asking to reset a users password
        """
        self.get_user_token(self.user)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'email': self.user['email']})
        url = '/auth/forgot-password'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_forgot_password_email_not_in_db(self):
        """
        Test requesting for password reset with email that has not account
        """
        self.get_user_token(self.user)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'email': self.other_user['email']})
        url = '/auth/forgot-password'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_forgot_password_invalid_email(self):
        """
        Test requesting password reset with invalid email
        """
        self.get_user_token(self.user)

        headers = {'content-type': 'application/json'}
        data = json.dumps({'email': ''})
        url = '/auth/forgot-password'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)
