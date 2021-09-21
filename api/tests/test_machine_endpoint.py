import json

from django.urls import reverse
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.test import APITestCase

from api import models

fake = Faker()

class MachineTests(APITestCase):
    """
    Tests CRUD operations on Machine endpoint.
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

    def test_create_machine(self):
        # login
        token = self.create_and_login_user()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        machines = models.Machine.objects.all()
        self.assertEqual(len(machines), 0)

        machine_details = {
            "ip_address": fake.ipv4(),
            "hostname": fake.hostname()
        }

        create_machine_url = reverse('machine-list')
        response = self.client.post(create_machine_url, data=machine_details)
        self.assertEqual(response.status_code, 201)
        machines = models.Machine.objects.all()
        self.assertEqual(len(machines), 1)

    def test_get_machines_list(self):
        list_machines_url = reverse('machine-list')
        # create 2 machines
        machine1 = models.Machine(ip_address=fake.ipv4(), hostname=fake.hostname())
        machine1.save()
        machine2 = models.Machine(ip_address=fake.ipv4(), hostname=fake.hostname())
        machine2.save()
        # login
        token = self.create_and_login_user()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(list_machines_url)
        self.assertEqual(response.json()['count'], 2) 