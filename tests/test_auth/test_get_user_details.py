from tests.base_test import BaseTestCase


class GetUserInfoTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/user'

    def add_user(self):
        """
        Create dummy user
        """
        return self.get_user_token(self.user)

    def test_get_user_info(self):
        """
        Test getting a users info
        """
        user_token = self.add_user()
        headers = {'Authorization': f'Bearer {user_token}',
                   'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_user_info_unauthenticated(self):
        """
        Test getting a users info
        """
        headers = {'content-type': 'application/json'}

        response = self.test_client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 401)
