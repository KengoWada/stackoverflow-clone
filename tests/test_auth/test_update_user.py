import json

from tests.base_test import BaseTestCase


class UpdateUserTestCase(BaseTestCase):

    def test_update_user_details(self):
        """
        Test updating a users detils
        """
        user_token = self.get_user_token(self.user)
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.update_user)
        url = '/auth/user'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 200)

    def test_update_user_invalid_request(self):
        """
        Test updating a users details with invalid body request
        """
        user_token = self.get_user_token(self.user)

        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps({})
        url = '/auth/user'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_user_with_existing_details(self):
        """
        Test updating a user with another users username and email
        """
        user_token = self.get_user_token(self.user)
        self.get_user_token(self.other_user)

        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        data = json.dumps(self.invalid_update_user)
        url = '/auth/user'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 400)

    def test_update_user_unauthenticated(self):
        """
        Test updating a user details when not logged in
        """
        self.get_user_token(self.user)
        headers = {'content-type': 'application/json'}
        data = json.dumps(self.update_user)
        url = '/auth/user'

        response = self.test_client.put(url, headers=headers, data=data)

        self.assertEqual(response.status_code, 401)
