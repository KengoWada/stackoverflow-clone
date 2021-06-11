import json

from tests.base_test import BaseTestCase


class UpdateQuestionTestCase(BaseTestCase):

    def add_question(self):
        """
        Create a dummy question
        """
        user_token = self.get_user_token(self.user)
        question_id = self.create_question(self.question, user_token)

        return user_token, question_id

    def test_update_question(self):
        """
        Test updating a question
        """
        user_token, question_id = self.add_question()
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_question)
        url = f'/questions/{question_id}'

        response = self.test_client.put(url, headers=headers, data=data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['question']['id'], question_id)

    def test_update_question_invalid_id(self):
        """
        Test updating a question with invalid ID
        """
        user_token, _ = self.add_question()
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_question)
        url = '/questions/0'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_question_invalid_request(self):
        """
        Test updating a question with invalid request body
        """
        user_token, question_id = self.add_question()
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.invalid_update_question)
        url = f'/questions/{question_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_question_not_authenticated(self):
        """
        Test updating a question when not logged in
        """
        _, quesion_id = self.add_question()
        headers = {'content-type': 'application/json'}
        data = json.dumps(self.update_question)
        url = f'/questions/{quesion_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)

    def test_update_question_not_authorized(self):
        """
        Test updatin another users questions
        """
        _, quesion_id = self.add_question()
        user_token = self.get_user_token(self.other_user)
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_question)
        url = f'/questions/{quesion_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 403)
