import json


from tests.base_test import BaseTestCase


class UpdateAnswerTestCase(BaseTestCase):

    def add_answer(self):
        """
        Create dummy question and answer
        """
        # Create users
        user = self.create_user(self.user)
        other_user = self.create_user(self.other_user)

        # Create question
        question = self.create_question(self.question, other_user.id)

        # Add answers
        answer = self.create_answer(self.answer, question.id, user.id)

        user_token = self.get_user_token(user)
        other_user_token = self.get_user_token(other_user)

        return user_token, other_user_token, question.id, answer.id

    def test_update_answer(self):
        """
        Test updating an answer
        """
        user_token, _, question_id, answer_id = self.add_answer()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_update_answer_invalid_question_id(self):
        """
        Test updating an answer with invalid question ID
        """
        user_token, _, _, answer_id = self.add_answer()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.update_answer)
        url = f'/questions/0/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_answer_invalid_answser_id(self):
        """
        Test updating an answer with invalid ID
        """
        user_token, _, question_id, _ = self.add_answer()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/0'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_answer_invalid_body(self):
        """
        Test updating an answer with invalid body
        """
        user_token, _, question_id, answer_id = self.add_answer()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.invalid_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_answer_unauthenticated(self):
        """
        Test updating an answer when not logged in
        """
        _, _, question_id, answer_id = self.add_answer()

        headers = self.get_request_header()
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)

    def test_update_answer_unauthorized(self):
        """
        Test updating another users answer
        """
        _, other_user_token, question_id, answer_id = self.add_answer()

        headers = self.get_request_header(other_user_token)
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 403)
