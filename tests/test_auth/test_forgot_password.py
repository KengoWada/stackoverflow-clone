import json

from tests.base_test import BaseTestCase


class ForgotPasswordTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/forgot-password'

    def test_forgot_password(self):
        """
        Test asking to reset a users password
        """
        self.create_user(self.user)

        headers = self.get_request_header()
        data = json.dumps({'email': self.user['email']})

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_forgot_password_email_not_in_db(self):
        """
        Test requesting for password reset with email that has not account
        """
        self.create_user(self.user)

        headers = self.get_request_header()
        data = json.dumps({'email': self.other_user['email']})

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_forgot_password_invalid_email(self):
        """
        Test requesting password reset with invalid email
        """
        self.create_user(self.user)

        headers = self.get_request_header()
        data = json.dumps({'email': ''})

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)
