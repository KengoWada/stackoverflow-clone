import json

from tests.base_test import BaseTestCase


class AddAnswerTestCase(BaseTestCase):

    def add_question(self):
        """
        Add a dummy question
        """
        user = self.create_user(self.user)
        question = self.create_question(self.question, user.id)

        return self.get_user_token(user), question.id

    def test_add_answer(self):
        """
        Test adding an answer to a question
        """
        _, question_id = self.add_question()

        user = self.create_user(self.other_user)
        user_token = self.get_user_token(user)

        headers = self.get_request_header(user_token)
        data = json.dumps(self.answer)
        url = f'/questions/{question_id}/answers'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 201)

    def test_add_answer_invalid_question_id(self):
        """
        Test adding an answer to an invalid question ID
        """
        user_token, _ = self.add_question()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.answer)
        url = '/questions/0/answers'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_add_answer_invalid_request(self):
        """
        Test adding an answer to an invalid request body
        """
        user_token, question_id = self.add_question()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.invalid_answer)
        url = f'/questions/{question_id}/answers'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_add_answer_unauthenticated(self):
        """
        Test adding an answer when not authenticated
        """
        _, question_id = self.add_question()

        headers = self.get_request_header()
        data = json.dumps(self.answer)
        url = f'/questions/{question_id}/answers'

        response = self.test_client.post(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)
