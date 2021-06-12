import json

from tests.base_test import BaseTestCase


class CreateQuestionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/'

    def add_user_return_user_token(self):
        """
        Add dummy user and return their JWT
        """
        user = self.create_user(self.user)
        return self.get_user_token(user)

    def test_create_question(self):
        """
        Test creating a question
        """
        user_token = self.add_user_return_user_token()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.question)

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 201)

    def test_create_question_not_authenticated(self):
        """
        Test creating a question without being logged in
        """
        headers = self.get_request_header()
        data = json.dumps(self.question)

        response = self.test_client.post(self.url, headers=headers, data=data)
        self.assertEqual(response.status_code, 401)

    def test_create_invalid_question(self):
        """
        Test creating invalid question
        """
        user_token = self.add_user_return_user_token()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.invalid_question)

        response = self.test_client.post(self.url, headers=headers, data=data)
        self.assertEqual(response.status_code, 400)
