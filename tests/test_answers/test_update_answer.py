import json


from tests.base_test import BaseTestCase


class UpdateAnswerTestCase(BaseTestCase):

    def add_answer(self):
        """
        Create dummy question and answer
        """
        # Create users
        user_token = self.get_user_token(self.user)
        other_user_token = self.get_user_token(self.other_user)

        # Create question
        question_id = self.create_question(self.question, user_token)

        # Add answers
        answer_id = self.create_answer(
            self.answer, question_id, other_user_token)

        return user_token, other_user_token, question_id, answer_id

    def test_update_answer(self):
        """
        Test updating an answer
        """
        _, other_user_token, question_id, answer_id = self.add_answer()

        headers = {'Authorization': f'Bearer {other_user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_update_answer_invalid_question_id(self):
        """
        Test updating an answer with invalid question ID
        """
        _, other_user_token, _, answer_id = self.add_answer()

        headers = {'Authorization': f'Bearer {other_user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_answer)
        url = f'/questions/0/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_answer_invalid_answser_id(self):
        """
        Test updating an answer with invalid ID
        """
        _, other_user_token, question_id, _ = self.add_answer()

        headers = {'Authorization': f'Bearer {other_user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/0'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    # TODO: Implement request validation
    # def test_update_answer_invalid_body(self):
    #     """
    #     Test updating an answer with invalid body
    #     """
    #     _, other_user_token, question_id, answer_id = self.add_answer()

    #     headers = {'Authorization': f'Bearer {other_user_token}',
    #                'content-type': 'application/json'}
    #     data = json.dumps(self.update_answer)
    #     url = f'/questions/{question_id}/answers/{answer_id}'

    #     response = self.test_client.put(url, headers=headers, data=data)

    #     self.assertEqual(response.status_code, 400)

    def test_update_answer_unauthenticated(self):
        """
        Test updating an answer when not logged in
        """
        _, _, question_id, answer_id = self.add_answer()

        headers = {'content-type': 'application/json'}
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)

    def test_update_answer_unauthorized(self):
        """
        Test updating another users answer
        """
        user_token, _, question_id, answer_id = self.add_answer()

        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_answer)
        url = f'/questions/{question_id}/answers/{answer_id}'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 403)
