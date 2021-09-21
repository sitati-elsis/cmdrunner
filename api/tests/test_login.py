import json

from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.test import APITestCase

from api import models

fake = Faker()

class UserLogin(APITestCase):
    """
    Tests that a user can login.
    """
    def test_user_login(self):
        # create user
        data = {
            'username': fake.user_name(),
            'password': fake.password(),
        }
        user = User.objects.create_user(**data)
        user.save()
        # login
        login_url = reverse('login')
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json()) 