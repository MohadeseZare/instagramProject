from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import User, UserSetting
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy


class UserViewTest(APITestCase):

    def test_login_superuser(self):
        user = User.objects.create_user('admin', get_user_model().objects.make_random_password(), is_staff=True)
        User.objects.create_user('client', get_user_model().objects.make_random_password())
        self.client.force_authenticate(user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(len(json), 2)

    def test_login_instagram_account(self):
        user = User.objects.create_user('client', get_user_model().objects.make_random_password())
        self.client.force_authenticate(user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(len(json), 1)

    def test_user_admin_list(self):
        mommy.make(get_user_model(), is_staff=True)
        mommy.make(get_user_model())
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(len(json), 2)

    def test_user_instagram_account_list(self):
        mommy.make(get_user_model())
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json = response.json()
        self.assertEqual(len(json), 1)

    def test_if_username_and_password_instagram_is_correct_then_signup(self):
        data = {'username': 'test.zare', 'password': '123Z456'}
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.last()
        self.assertEqual(user.username, data['username'])
        self.assertEquals(user.check_password(data['password']), True)
        self.assertNotEqual(user.instagram_user_id, '')
        self.assertEqual(User.objects.count(), 3)

    def test_if_username_and_password_instagram_is_not_correct_then_signup(self):
        data = {'username': 'test.zare', 'password': get_user_model().objects.make_random_password()}
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'Wrong username or password.')

    def test_user_setting_update(self):
        user = User.objects.create_user('client', get_user_model().objects.make_random_password())
        self.client.force_login(user)
        user_setting = UserSetting.objects.get(user=user)
        data = {
            "id": user.id,
            "number_of_followers_per_hour": 5,
            "number_of_followers_per_day": 200,
            "number_of_unfollowers_per_day": 70,
            "number_of_likes_per_hour": 300,
            "number_of_likes_per_day": 7000,
            "number_of_comments_per_hour": 59,
            "number_of_comments_per_day": 500,
            "number_of_hashtags_used_in_the_post": 30,
            "number_of_caption_words": 2200,
            "number_of_comment_words": 240
        }
        response = self.client.patch(reverse('user_setting'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_setting = UserSetting.objects.get(user=user)
        self.assertEqual(user_setting.number_of_followers_per_hour, data['number_of_followers_per_hour'])
