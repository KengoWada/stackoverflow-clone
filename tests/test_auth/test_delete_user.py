from tests.base_test import BaseTestCase


class DeleteUserTestCase(BaseTestCase):

    def test_delete_user(self):
        """
        Test deleting a user
        """
        user_token = self.get_user_token(self.user)
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}
        url = '/auth/user'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_user_unauthenticated(self):
        """
        Test deleting a user when not logged in
        """
        self.get_user_token(self.user)
        headers = {'content-type': 'application/json'}
        url = '/auth/user'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 401)
