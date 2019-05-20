from django.test import TestCase
from graphene.test import Client

from ..schema.schema import schema


class GraphQLTestCase(TestCase):

    def setUp(self):
        self._client = Client(schema=schema)

    def send_graphql_request(self, graphql_query):
        response = self._client.execute(graphql_query)
        return response

    @staticmethod
    def handle_graphql_response(response, query_name):
        assert "errors" not in response
        return response["data"][query_name]
