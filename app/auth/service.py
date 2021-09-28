from typing import Optional

from django.contrib.auth import models as auth_models
from rest_framework.authtoken.models import Token

from app import models


def signin(user: auth_models.User):
    # delete old token
    try:
        user.auth_token.delete()
    except auth_models.User.auth_token.RelatedObjectDoesNotExist:
        pass

    # create new one
    token, created = Token.objects.get_or_create(user=user)
    return token


def signup(
    *,
    username: str,
    password: str,
    email: str,
    first_name: str,
    last_name: str,
    phone: str,
    country: Optional[int],
    province: str,
    city: str
) -> auth_models.User:
    user = auth_models.User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    models.UserInfo.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        country_id=country,
        province=province,
        phone=phone,
        city=city,
    )
    return user
