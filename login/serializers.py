from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth import login
from rest_framework import serializers
from instagram_private_api import Client


UserModel = get_user_model()
class LoginSerializer(serializers.Serializer):
    """Serializer for loggin in.
       It checks username and password are correct for settings.AUTH_USER_MODEL.

       After validating it, ``user`` instance created for authenticated user.
       View methods should persist this user.
       (through ``django.contrib.auth.login``)

       :param username: ``USERNAME_FIELD`` for AUTH_USER_MODEL
       :param password: user's password
       """
    username = serializers.CharField(
        label=('Username'), max_length=254,
    )

    password = serializers.CharField(
        label=('Password'), write_only=True,
        style={'input_type': 'password'},
    )

    default_error_messages = {
        'invalid_login': (
            'Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.'
        ),
        'inactive': ('This account is inactive.'),
    }

    def validate(self, data):
        """Checks username & password.
        uses ``django.contrib.auth.authenticate``

        :param data: validated data from ``Serializer.validate``
        :return: validated_data
        :exception VaildationError: if username or password are incorrect
        """
        username = data['username']
        password = data['password']

        self.user = auth.authenticate(username=username, password=password)
        if self.user is None:
            raise serializers.ValidationError(
                self.error_messages['invalid_login'], code='invalid_login',
            )

        self.confirm_login_allowed(self.user)

        return data

    def confirm_login_allowed(self, user):
        current_user = 0
        # api = Client(current_user.username, current_user.instagram_password)
        # cache.set('instagram_api', api)

    def create(self, validated_data):
        """persist a authenticated user in this step.

        :param validated_data: validated_data should contains ``request``.\
        You should pass request to serialzer.save.
        """
        user = self.get_user()
        request = validated_data.get('request')
        self.perform_login(request, user)

        return user

    def perform_login(self, request, user):
        """Persist a user. Override this method if you do more than
        persisting user.
        """
        login(request, user)

    def get_user(self):
        """
        :return: ``user`` instance created after ``self.validate``
        """
        return self.user

