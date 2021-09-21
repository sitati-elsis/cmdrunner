import json

from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.test import APITestCase

from api import models

fake = Faker()


# Create your tests here.
class Signup(APITestCase):
    """
    Tests that a user can signup.
    """
    def test_user_can_signup(self):
        """
        Test that user can signup.
        """
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        signup_url = reverse('signup-list')

        user = {
            "username": fake.user_name(),
            "password": fake.password()
        }
        response = self.client.post(signup_url, user)
        self.assertEqual(response.status_code, 201)
        users = User.objects.all()
        self.assertEqual(len(users), 1)