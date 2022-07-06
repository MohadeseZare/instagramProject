from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from user.models import User, UserSetting


class UserModelTest(APITestCase):

    def test_save_user_setting_before_save_user(self):
        user = User.objects.create_user('client', get_user_model().objects.make_random_password())
        user_setting = UserSetting.objects.filter(user=user)
        self.assertEqual(user_setting.count(), 1)
