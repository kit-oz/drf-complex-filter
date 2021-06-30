from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from mixer.backend.django import mixer

from .models import TestCaseModel


class DynaimcFilterTests(APITestCase):
    URL = "/test/"

    def setUp(self):
        user1 = mixer.blend(User, username="user1", password="password1")
        user2 = mixer.blend(User, username="user2", password="password2")
        mixer.blend(TestCaseModel, user=user1)
        mixer.blend(TestCaseModel, user=user2)
        mixer.blend(TestCaseModel)

        self.user = user1

    def test_me(self):
        query = {"filters": "userISME"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=f"Failed on: {query}" f"\nResponse: {response.data}"
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_not_me(self):
        query = {"filters": "userISNOTME"}
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=f"Failed on: {query}" f"\nResponse: {response.data}"
        )
        self.assertEqual(len(response.data), 2)
        for result in response.data:
            self.assertNotEqual(result["user"], self.user.id)

    def test_me_unauthenticated(self):
        query = {"filters": "userISME"}
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=f"Failed on: {query}" f"\nResponse: {response.data}"
        )
        self.assertEqual(len(response.data), 1)
        self.assertIsNone(response.data[0]["user"])

    def test_not_me_unauthenticated(self):
        query = {"filters": "userISNOTME"}
        response = self.client.get(self.URL, query, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=f"Failed on: {query}" f"\nResponse: {response.data}"
        )
        self.assertEqual(len(response.data), 2)
        for result in response.data:
            self.assertIsNotNone(result["user"])
