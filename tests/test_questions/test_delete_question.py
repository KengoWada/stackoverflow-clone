import json

from tests.base_test import BaseTestCase


class DeleteQuestionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/'

    def add_question_return_user_token_question_id(self):
        """
        Add a dummy question and return user_token, question_id
        """
        user = self.create_user(self.user)
        question = self.create_question(self.question, user.id)

        return self.get_user_token(user), question.id

    def test_delete_question(self):
        """
        Test deleting a question
        """
        user_token, question_id = self.add_question_return_user_token_question_id()

        headers = self.get_request_header(user_token)
        url = f'{self.url}{question_id}'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_question_invalid_id(self):
        """
        Test deleting a question with an invalid ID
        """
        user_token, _ = self.add_question_return_user_token_question_id()

        headers = self.get_request_header(user_token)
        url = f'{self.url}0'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_delte_question_not_authenticated(self):
        """
        Test deleting a question when not logged in
        """
        _, quesion_id = self.add_question_return_user_token_question_id()

        headers = self.get_request_header()
        data = json.dumps(self.update_question)
        url = f'{self.url}{quesion_id}'

        response = self.test_client.delete(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)

    def test_delete_question_not_authorized(self):
        """
        Test deleting another users questions
        """
        _, quesion_id = self.add_question_return_user_token_question_id()

        other_user = self.create_user(self.other_user)
        other_user_token = self.get_user_token(other_user)

        headers = self.get_request_header(other_user_token)
        url = f'{self.url}{quesion_id}'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 403)
