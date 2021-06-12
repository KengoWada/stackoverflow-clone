import unittest

from flask_jwt_extended import create_access_token

from api import create_app, db
from api.models import Question, User, Answer
from api.utils import get_token
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
        self.user_login = {'username': 'SomePerson',
                           'password': 'complex_password'}
        self.invalid_user = {
            'username': 'SomePerson', 'password': 'password'}
        self.invalid_register_user = {
            'username': 'SomePerson', 'email': 'some@'}
        self.update_user = {'email': 'some@email.com',
                            'username': 'UpdatedUsername'}
        self.invalid_update_user = {'email': 'some@email.com',
                                    'username': 'OtherUser'}
        self.other_user = {'username': 'OtherUser',
                           'email': 'other@email.com', 'password': 'complex_password'}

        # Dummy questions
        self.question = {'title': 'Sample question',
                         'body': 'Sample question body'}
        self.invalid_question = {}
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

    def create_user(self, data):
        """
        Create a dummy user
        """
        user = User(email=data['email'], username=data['username'])
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return user

    def get_user_token(self, user):
        """
        Return valid token for user provided
        """
        return create_access_token(identity=user)

    def set_password_reset_token(self, user, token):
        """
        Set the password reset token for provided user
        """
        user.password_reset_token = token
        db.session.commit()

    def create_question(self, data, user_id):
        """
        Create a dummy question for the user_id provided
        """
        question = Question(title=data['title'],
                            body=data['body'], user_id=user_id)
        db.session.add(question)
        db.session.commit()

        return question

    def create_answer(self, data, question_id, user_id):
        """
        Create a dummy answer for the user_id and question_id provided
        """
        answer = Answer(body=data['body'],
                        question_id=question_id, user_id=user_id)
        db.session.add(answer)
        db.session.commit()

        return answer

    def get_request_header(self, user_token=None):
        """
        Return header for making requests
        """
        headers = {'content-type': 'application/json'}

        if user_token:
            headers['Authorization'] = f'Bearer {user_token}'

        return headers

    def get_user_password_token(self, email):
        return get_token(email)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
