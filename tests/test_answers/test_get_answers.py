import json


from tests.base_test import BaseTestCase


class GetAnswersTestCase(BaseTestCase):

    def add_answers(self):
        """
        Add a dummy question and answers
        """
        # Create users
        user_token = self.get_user_token(self.user)
        other_user_token = self.get_user_token(self.other_user)

        # Create question
        question_id = self.create_question(self.question, user_token)

        # Add answers
        self.create_answer(self.answer, question_id, other_user_token)
        self.create_answer(self.other_answer, question_id, user_token)

        return question_id

    def test_get_question_answers(self):
        """
        Test getting answers for a question
        """
        question_id = self.add_answers()

        headers = {'content-type': 'application/json'}
        url = f'/questions/{question_id}/answers'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_answers_invalid_question_id(self):
        """
        Test getting answers for invalid question ID
        """
        headers = {'content-type': 'application/json'}
        url = '/questions/0/answers'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)


class GetAnswerTestCase(BaseTestCase):

    def add_answer(self):
        """
        Add a dummy question and answers
        """
        # Create users
        user_token = self.get_user_token(self.user)
        other_user_token = self.get_user_token(self.other_user)

        # Create question
        question_id = self.create_question(self.question, user_token)

        # Add answers
        answer_id = self.create_answer(
            self.answer, question_id, other_user_token)

        return question_id, answer_id

    def test_get_answer(self):
        """
        Test getting an answer
        """
        question_id, answer_id = self.add_answer()

        headers = {'content-type': 'application/json'}
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_answer_invalid_question_id(self):
        """
        Test getting an answer for a wrong question ID
        """
        _, answer_id = self.add_answer()

        headers = {'content-type': 'application/json'}
        url = f'/questions/0/answers/{answer_id}'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)
