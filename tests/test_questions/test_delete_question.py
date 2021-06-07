import json

from tests.base_test import BaseTestCase


class DeleteQuestionTestCase(BaseTestCase):

    def add_question(self):
        """
        Create a dummy question
        """
        user_token = self.get_user_token(self.user)
        question_id = self.create_question(self.question, user_token)

        return user_token, question_id

    def test_delete_question(self):
        """
        Test deleting a question
        """
        user_token, question_id = self.add_question()
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        url = f'/questions/{question_id}'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 200)

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_delete_question_invalid_id(self):
        """
        Test deleting a question with an invalid ID
        """
        user_token, _ = self.add_question()
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        url = '/questions/0'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_delte_question_not_authenticated(self):
        """
        Test deleting a question when not logged in
        """
        _, quesion_id = self.add_question()
        headers = {'content-type': 'application/json'}
        data = json.dumps(self.update_question)
        url = f'/questions/{quesion_id}'

        response = self.test_client.delete(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)

    def test_delete_question_not_authorized(self):
        """
        Test updatin another users questions
        """
        _, quesion_id = self.add_question()
        user_token = self.get_user_token(self.other_user)
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        url = f'/questions/{quesion_id}'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 403)
