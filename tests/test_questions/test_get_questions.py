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
        user = self.create_user(self.user)
        other_user = self.create_user(self.other_user)

        # Add questions
        self.create_question(self.question, user.id)
        self.create_question(self.other_question, other_user.id)

    def test_get_questions(self):
        """
        Test getting all questions
        """
        self.add_questions()

        headers = self.get_request_header()

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(data['questions']), 1)

    def test_get_questions_empty(self):
        """
        Test get questions with empty db
        """
        headers = self.get_request_header()

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['questions']), 0)


class GetMyQuestionsTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/mine'

    def add_my_questions(self):
        """
        Add questions for user
        """
        user = self.create_user(self.user)

        self.create_question(self.question, user.id)
        self.create_question(self.other_question, user.id)

        return self.get_user_token(user=user)

    def test_get_user_questions(self):
        """
        Test getting questions posted by a user
        """
        user_token = self.add_my_questions()

        headers = self.get_request_header(user_token)

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(data['questions']), 1)

    def test_get_questions_empty(self):
        """
        Test getting questions when user has none
        """
        user = self.create_user(self.other_user)
        user_token = self.get_user_token(user)

        headers = self.get_request_header(user_token)

        response = self.test_client.get(self.url, headers=headers)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['questions']), 0)

    def test_get_user_questions_unauthenticated(self):
        """
        Test getting a users questions when not logged in
        """
        self.add_my_questions()

        headers = self.get_request_header()

        response = self.test_client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 401)


class GetQuestionTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/questions/'

    def add_question(self):
        """
        Create dummy questions
        """
        user = self.create_user(self.user)

        question = self.create_question(self.question, user.id)

        return question.id

    def test_get_question_by_id(self):
        """
        Test getting a question by its ID
        """
        question_id = self.add_question()

        headers = self.get_request_header()
        url = f'{self.url}{question_id}'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_question_invalid_id(self):
        """
        Test getting a question with an invalid ID
        """
        self.add_question()

        headers = self.get_request_header()
        url = f'{self.url}0'

        response = self.test_client.get(url, headers=headers)

        self.assertEqual(response.status_code, 400)
