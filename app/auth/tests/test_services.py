from django.contrib.auth.models import User
from django.test import TestCase

from app.auth.service import signin


class TestSignin(TestCase):
    def test_signin(self):
        user = User.objects.create_user(
            username="juan",
            password="juna",
            email="juan@j.com"
        )
        token = signin(user)
        assert token is not None
