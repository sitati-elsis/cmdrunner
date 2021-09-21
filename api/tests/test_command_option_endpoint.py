import json
import random

from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.test import APITestCase

from api import models

fake = Faker()

class CommandOptionTests(APITestCase):
    """
    Tests CRUD operations on CommandOptions endpoint.
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

    def test_create_commandoption(self):
        # login
        token = self.create_and_login_user()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        command_options = models.CommandOptions.objects.all()
        self.assertEqual(len(command_options), 0)

        choices = tuple([letter for letter in 'abcdefghijklmnopqrstuvwxyz'])
        co_details = {
            "option": random.choice(choices),
            "description": fake.sentence()
        }
        command = models.Command(command_name=fake.word())
        command.save()
        create_co_url = reverse('commandoptions-list',
                            kwargs={'command_pk': command.command_id})
        response = self.client.post(create_co_url, data=co_details)
        self.assertEqual(response.status_code, 201)
        command_options = models.CommandOptions.objects.all()
        self.assertEqual(len(command_options), 1)
        self.assertEqual(command_options[0].command, command)

    def test_list_command_options(self):
        # login
        token = self.create_and_login_user()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        # creaet command
        command = models.Command(command_name=fake.word())
        command.save()
        # create options
        co1 = models.CommandOptions(
            option='a', description=fake.sentence(), command=command)
        co1.save()
        co2 = models.CommandOptions(
            option='z', description=fake.sentence(), command=command)
        co2.save()
        co_list_url = reverse('commandoptions-list',
                            kwargs={'command_pk': command.command_id})
        response = self.client.get(co_list_url)
        self.assertEqual(response.json()['count'], 2)