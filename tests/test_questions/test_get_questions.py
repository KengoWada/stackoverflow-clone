import json

from tests.base_test import BaseTestCase


class GetQuestionsTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/'

    def add_questions(self):
        """
        Add dummy questions to the database
        """
        # Add users
        user_token = self.get_user_token(self.user)
        user2_token = self.get_user_token(self.other_user)

        # Add questions
        self.create_question(self.question, user_token)
        self.create_question(self.other_question, user2_token)

    def test_get_questions(self):
        """
        Test getting all questions
        """
        self.add_questions()

        headers = {'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(data['questions']), 1)

    def test_get_questions_empty(self):
        """
        Test get questions with empty db
        """
        headers = {'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['questions']), 0)


class GetMyQuestionsTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/mine'

    def add_questions(self):
        """
        Add questions for user
        """
        user_token = self.get_user_token(self.user)

        self.create_question(self.question, user_token)
        self.create_question(self.other_question, user_token)

        return user_token

    def test_get_user_questions(self):
        """
        Test getting questions posted by a user
        """
        token = self.add_questions()
        headers = {'Authorization': f'Bearer {token}',
                   'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(data['questions']), 1)

    def test_get_questions_empty(self):
        """
        Test getting questions when user has none
        """
        token = self.get_user_token(self.user)
        headers = {'Authorization': f'Bearer {token}',
                   'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['questions']), 0)

    def test_get_user_questions_unauthenticated(self):
        """
        Test getting a users questions when not logged in
        """
        self.add_questions()
        headers = {'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 401)


class GetQuestionTestCase(BaseTestCase):

    def add_question(self):
        """
        Create dummy questions
        """
        user_token = self.get_user_token(self.user)

        question_id = self.create_question(self.question, user_token)

        return question_id

    def test_get_question_by_id(self):
        """
        Test getting a question by its ID
        """
        question_id = self.add_question()

        headers = {'content-type': 'application/json'}
        url = f'/questions/{question_id}'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_question_invalid_id(self):
        """
        Test getting a question with an invalid ID
        """
        self.add_question()

        headers = {'content-type': 'application/json'}
        url = '/questions/0'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)
