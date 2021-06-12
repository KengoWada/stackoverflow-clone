import json

from tests.base_test import BaseTestCase


class UpdateUserTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/user'

    def add_user_return_user_token(self):
        """
        Add a dummy user and return their token
        """
        user = self.create_user(self.user)
        return self.get_user_token(user)

    def test_update_user_details(self):
        """
        Test updating a users detils
        """
        user_token = self.add_user_return_user_token()

        headers = self.get_request_header(user_token)
        data = json.dumps(self.update_user)

        response = self.test_client.put(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_update_user_invalid_request(self):
        """
        Test updating a users details with invalid body request
        """
        user_token = self.add_user_return_user_token()

        headers = self.get_request_header(user_token)
        data = json.dumps({})

        response = self.test_client.put(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_user_with_existing_details(self):
        """
        Test updating a user with another users username and email
        """
        user_token = self.add_user_return_user_token()
        self.create_user(self.other_user)

        headers = self.get_request_header(user_token)
        data = json.dumps(self.invalid_update_user)

        response = self.test_client.put(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_user_unauthenticated(self):
        """
        Test updating a user details when not logged in
        """
        self.create_user(self.user)

        headers = self.get_request_header()
        data = json.dumps(self.update_user)

        response = self.test_client.put(self.url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)
