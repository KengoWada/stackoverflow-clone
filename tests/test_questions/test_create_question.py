import json

from tests.base_test import BaseTestCase


class CreateQuestionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/'

    def test_create_question(self):
        """
        Test creating a question
        """
        token = self.get_user_token(self.user)
        headers = {'Authorization': f'Bearer {token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.question)

        response = self.test_client.post(self.url, headers=headers, data=data)
        self.assertEqual(response.status_code, 201)

    def test_create_question_not_authenticated(self):
        """
        Test creating a question without being logged in
        """
        headers = {'content-type': 'application/json'}
        data = json.dumps(self.question)

        response = self.test_client.post(self.url, headers=headers, data=data)
        self.assertEqual(response.status_code, 401)

    # def test_create_invalid_question(self):
    #     """
    #     Test creating invalid question
    #     """
    #     token = self.get_user_token(self.user)
    #     headers = {'Authorization': f'Bearer {token}',
    #                'content-type': 'application/json'}
    #     data = json.dumps(self.invalid_question)

    #     response = self.test_client.post(self.url, headers=headers, data=data)
    #     self.assertEqual(response.status_code, 400)
