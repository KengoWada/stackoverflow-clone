import json

from tests.base_test import BaseTestCase


class LikeDislikeAnswerTestCase(BaseTestCase):

    def add_answer(self):
        """
        Add a dummy question and answer
        """
        # Create users
        user = self.create_user(self.user)
        other_user = self.create_user(self.other_user)

        # Create question
        question = self.create_question(self.question, user.id)

        # Add answers
        answer = self.create_answer(self.answer, question.id, other_user.id)

        return self.get_user_token(user), question.id, answer.id

    def test_liking_answer(self):
        """
        Test liking an answer
        """
        user_token, question_id, answer_id = self.add_answer()

        headers = self.get_request_header(user_token)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.patch(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_disliking_answer(self):
        """
        Test disliking an answer
        """
        user_token, question_id, answer_id = self.add_answer()

        headers = self.get_request_header(user_token)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.patch(url, headers=headers)

        self.assertEqual(response.status_code, 200)

        response = self.test_client.patch(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_liking_answer_unauthorized(self):
        """
        Test liking an answer when not authenticated
        """
        _, question_id, answer_id = self.add_answer()

        headers = self.get_request_header()
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.patch(url, headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_liking_answer_invalid_question_id(self):
        """
        Test liking an answer with an invalid question ID
        """
        user_token, _, answer_id = self.add_answer()

        headers = self.get_request_header(user_token)
        url = f'/questions/0/answers/{answer_id}'

        response = self.test_client.patch(url, headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_liking_answer_invalid_id(self):
        """
        Test liking an answer with an invalid ID
        """
        user_token, question_id, _ = self.add_answer()

        headers = self.get_request_header(user_token)
        url = f'/questions/{question_id}/answers/0'

        response = self.test_client.patch(url, headers=headers)

        self.assertEqual(response.status_code, 400)
