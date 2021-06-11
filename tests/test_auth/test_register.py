import json

from tests.base_test import BaseTestCase


class ResgistrationTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/register'

    def test_user_registration(self):
        """
        Test registering a user
        """
        response = self.test_client.post(
            self.url, content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code, 201)

    def test_registering_twice(self):
        """
        Test registering with same email and/or username
        """
        response = self.test_client.post(
            self.url, content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code, 201)

        response = self.test_client.post(
            self.url, content_type='application/json', data=json.dumps(self.user))
        self.assertEqual(response.status_code, 400)

    def test_registering_invalid_request(self):
        """
        Test registering with an invalid request body
        """
        headers = {'content-type': 'application/json'}
        data = json.dumps(self.invalid_register_user)

        response = self.test_client.post(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)
