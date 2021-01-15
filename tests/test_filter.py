from rest_framework.test import APITestCase
from rest_framework import status
from parameterized import parameterized

from .models import TestCaseModel
from .fixtures import RECORDS
from .test_data import TEST_DATA


class ComplexFilterTests(APITestCase):
    URL = "/test/"

    def setUp(self):
        for record in RECORDS:
            record = TestCaseModel(**record)
            record.save()

    @parameterized.expand(TEST_DATA)
    def test_filter(self, query, expected_response):
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}")
        self.assertEqual(len(response.data), len(expected_response),
                         msg=f"Failed on: {query}"
                             f"\nResponse: {response.data}"
                             f"\nExpected: {expected_response}")
        for result in response.data:
            self.assertIn(result, expected_response,
                          msg=f"Failed on: {query}"
                              f"\nResponse: {response.data}"
                              f"\nExpected: {expected_response}")
