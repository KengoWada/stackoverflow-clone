from tests.base_test import BaseTestCase


class GetUserInfoTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = '/auth/user'

    def test_get_user_info(self):
        """
        Test getting a users info
        """
        user = self.create_user(self.user)
        user_token = self.get_user_token(user=user)

        headers = self.get_request_header(user_token)

        response = self.test_client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_get_user_info_unauthenticated(self):
        """
        Test getting a users info
        """
        headers = self.get_request_header()

        response = self.test_client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, 401)
