from tests.base_test import BaseTestCase


class DeleteUserTestCase(BaseTestCase):

    def add_user_return_token(self):
        """
        Create a dummy user and return their JWT
        """
        user = self.create_user(self.user)
        return self.get_user_token(user)

    def test_delete_user(self):
        """
        Test deleting a user
        """
        user_token = self.add_user_return_token()

        headers = self.get_request_header(user_token)
        url = '/auth/user'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_delete_user_unauthenticated(self):
        """
        Test deleting a user when not logged in
        """
        self.add_user_return_token()

        headers = self.get_request_header()
        url = '/auth/user'

        response = self.test_client.delete(url, headers=headers)

        self.assertEqual(response.status_code, 401)
