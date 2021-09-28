import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from app.auth.service import signin
from app.auth.service import signup
from app.models import UserInfo


class TestSignin(TestCase):
    def test_signin(self):
        user = User.objects.create_user(
            username="juan", password="juna", email="juan@j.com"
        )
        token = signin(user)
        assert token is not None


@pytest.mark.django_db
def test_signup():
    user = signup(
        username="juan",
        password="juna",
        email="juan@j.com",
        first_name="juan",
        last_name="senn",
        phone="+543513840245",
        country=None,
        province="Cordoba",
        city="Capital",
    )
    additional_info = UserInfo.objects.get(user=user)
    assert isinstance(user, User)
    assert additional_info.first_name == "juan"
