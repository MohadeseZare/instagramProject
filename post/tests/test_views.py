from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class PostViewTest(APITestCase):
    def setUp(self):
        data = {'username': 'test.zare', 'password': '123Z456'}
        self.client.post(reverse('user-list'), data)
        self.user = User.objects.get(username='test.zare')
        self.client.force_authenticate(self.user)

    def test_get_post_current_user(self):
        pass

    def test_get_time_line(self):
        pass

    def test_like_post(self):
        pass

    def test_unlike_post(self):
        pass

    def test_get_comment_post(self):
        pass

    def test_create_new_comment_for_post(self):
        pass

    def test_deleted_comment(self):
        pass

    def test_like_comment(self):
        pass

    def test_unlike_comment(self):
        pass
