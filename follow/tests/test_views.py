from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class FollowViewTest(APITestCase):
    def setUp(self):
        data = {'username': 'test.zare', 'password': '123Z456'}
        self.client.post(reverse('user-list'), data)
        self.user = User.objects.get(username='test.zare')
        self.client.force_authenticate(self.user)

    def test_new_follow(self):
        response = self.client.post(reverse('follow', kwargs={'username': 'radiowland'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_follower(self):
        self.client.post(reverse('follow', kwargs={'username': 'radiowland'}))
        response = self.client.delete(reverse('un_follow', kwargs={'username': 'radiowland'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_follower(self):
        response = self.client.get(reverse('followers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_following(self):
        response = self.client.get(reverse('following'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
