from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import User
from rest_framework.test import APITestCase


class LoginTest(APITestCase):

    def test_login_admin(self):
        user = User.objects.create_user('username', get_user_model().objects.make_random_password(), is_staff=True)
        self.data = {"username": user.username, "password": user.password}
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Unable to log in with provided credentials.')

    def test_login_instagram_account(self):
        user = User.objects.create_user('username', get_user_model().objects.make_random_password(),
                                        instagram_user_id=53834993293)
        self.data = {"username": user.username, "password": user.password}
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Unable to log in with provided credentials.')

    def test_not_registered_username(self):
        user = User.objects.create_user('username', get_user_model().objects.make_random_password())
        self.data = {"username": 'user1', "password": user.password}
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'username is not registered.')
        pass

    def test_incorrect_username_or_password(self):
        user = User.objects.create_user('username', get_user_model().objects.make_random_password())
        self.data = {"username": user.username, "password": '123'}
        response = self.client.post(reverse('login'), self.data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Must include "username" and "password".')
        pass
