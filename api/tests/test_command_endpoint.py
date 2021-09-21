import json

from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.test import APITestCase

from api import models

fake = Faker()

class CommandTests(APITestCase):
    """
    Tests CRUD operations on Command endpoint.
    """
    def create_and_login_user(self):
        """`
        helper method to create a user and log them in.
        """
        data = {
                'username': fake.user_name(),
                'password': fake.password(),
            }
        user = User.objects.create_user(**data)
        user.save()
        login_url = reverse('login')
        response = self.client.post(login_url, data)
        return response.json()

    def test_create_command(self):
        # login
        token = self.create_and_login_user()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        commands = models.Command.objects.all()
        self.assertEqual(len(commands), 0)

        command_details = {
            "command_name": fake.word()
        }

        create_command_url = reverse('command-list')
        response = self.client.post(create_command_url, data=command_details) 
        self.assertEqual(response.status_code, 201)
        commands = models.Command.objects.all()
        self.assertEqual(len(commands), 1)

    def test_get_commands_list(self):
        list_commands_url = reverse('command-list')
        # create 2 command
        command1 = models.Command(command_name=fake.word())
        command1.save()
        command2 = models.Command(command_name=fake.word())
        command2.save()
        # login
        token = self.create_and_login_user()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(list_commands_url)
        self.assertEqual(response.json()['count'], 2) 