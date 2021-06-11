import json
import unittest


from api import create_app, db
from config import TestConfig


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.test_client = self.app.test_client()
        self.app_context.push()

        db.create_all()

        # Dummy users
        self.user = {'username': 'SomePerson',
                     'email': 'some@email.com', 'password': 'complex_password'}
        self.invalid_user = {
            'username': 'SomePerson', 'password': 'password'}
        self.invalid_register_user = {
            'username': 'SomePerson', 'email': 'some@'}
        self.other_user = {'username': 'OtherUser',
                           'email': 'other@email.com', 'password': 'complex_password'}

        # Dummy questions
        self.question = {'title': 'Sample question',
                         'body': 'Sample question body'}
        self.invalid_question = {'title': 'Invalid question'}
        self.update_question = {
            'title': 'New sample question', 'body': 'New sample question body'}
        self.invalid_update_question = {}
        self.other_question = {
            'title': 'Other question', 'body': 'Other question body'}

        # Dummy answers
        self.answer = {'body': 'A cool answer'}
        self.update_answer = {'body': 'An updated cool answer'}
        self.invalid_answer = {}
        self.other_answer = {'body': 'Other cool answer'}

    def get_user_token(self, user_data):
        """
        Create dummy user and return JWT
        """
        headers = {'content-type': 'application/json'}
        data = json.dumps(user_data)
        url = '/auth/register'

        response = self.test_client.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 201)

        url = '/auth/login'

        response = self.test_client.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())
        return data['access_token']

    def create_question(self, question_data, token):
        """
        Create a question for user whose token is provided and return question id
        """
        headers = {'Authorization': f'Bearer {token}',
                   'content-type': 'application/json'}
        data = json.dumps(question_data)
        url = '/questions/'

        response = self.test_client.post(url, headers=headers, data=data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        return data['question']['id']

    def create_answer(self, answer_data, question_id, token):
        """
        Create an answer for a question and user whose token is provided
        """
        headers = {'Authorization': f'Bearer {token}',
                   'content-type': 'application/json'}
        data = json.dumps(answer_data)
        url = f'/questions/{question_id}/answers'

        response = self.test_client.post(url, headers=headers, data=data)
        data = json.loads(response.data.decode())

        return data['answer']['id']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
