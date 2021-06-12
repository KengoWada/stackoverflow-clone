import json


from tests.base_test import BaseTestCase


class GetAnswersTestCase(BaseTestCase):

    def add_answers(self):
        """
        Add a dummy question and answers
        """
        # Create users
        user = self.create_user(self.user)
        other_user = self.create_user(self.other_user)

        # Create question
        question = self.create_question(self.question, user.id)

        # Add answers
        self.create_answer(self.answer, question.id, other_user.id)
        self.create_answer(self.other_answer, question.id, user.id)

        return question.id

    def test_get_question_answers(self):
        """
        Test getting answers for a question
        """
        question_id = self.add_answers()

        headers = self.get_request_header()
        url = f'/questions/{question_id}/answers'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_answers_invalid_question_id(self):
        """
        Test getting answers for invalid question ID
        """
        headers = self.get_request_header()
        url = '/questions/0/answers'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)


class GetAnswerTestCase(BaseTestCase):

    def add_answer(self):
        """
        Add a dummy question and answers
        """
        # Create users
        user = self.create_user(self.user)
        other_user = self.create_user(self.other_user)

        # Create question
        question = self.create_question(self.question, user.id)

        # Add answers
        answer = self.create_answer(self.answer, question.id, other_user.id)

        return question.id, answer.id

    def test_get_answer(self):
        """
        Test getting an answer
        """
        question_id, answer_id = self.add_answer()

        headers = self.get_request_header()
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_answer_invalid_question_id(self):
        """
        Test getting an answer for a wrong question ID
        """
        _, answer_id = self.add_answer()

        headers = self.get_request_header()
        url = f'/questions/0/answers/{answer_id}'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)
