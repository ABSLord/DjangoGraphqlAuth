from django.contrib.auth import get_user_model

from ..tests.base import GraphQLTestCase


class TestJWTAuth(GraphQLTestCase):

    gwt_token = None

    def setUp(self):
        super().setUp()
        self._username = "noname"
        self._password = "qwerty"
        self._test_user = get_user_model().objects.create_user(self._username,
                                                               "",
                                                               self._password)

    def test_token_auth_mutation(self):
        mutation = 'mutation {{tokenAuth(username:"{}", password:"{}"){{token}}}}'.format(self._username, self._password)
        response = self.send_graphql_request(mutation)
        response_data = self.handle_graphql_response(response, "tokenAuth")
        token = response_data.get("token", None)
        assert token
        TestJWTAuth.jwt_token = token

    def _test_verify_token_mutation(self):
        assert TestJWTAuth.jwt_token
        mutation = 'mutation {{verifyToken(token: "{}"){{payload}}}}'.format(
            TestJWTAuth.jwt_token)
        response = self.send_graphql_request(mutation)
        response_data = self.handle_graphql_response(response, "verifyToken")
        payload = response_data.get("payload", None)
        assert payload
        username = payload.get("username", None)
        assert username == self._username

    def _test_token_refresh_mutation(self):
        assert TestJWTAuth.jwt_token
        mutation = 'mutation {{refreshToken(token: "{}"){{token}}}}'.format(
            TestJWTAuth.jwt_token)
        response = self.send_graphql_request(mutation)
        response_data = self.handle_graphql_response(response, "refreshToken")
        token = response_data.get("token", None)
        assert token
