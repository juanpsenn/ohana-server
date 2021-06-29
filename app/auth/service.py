from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def signin(user: User):
    # delete old token
    user.auth_token.delete()
    # create new one
    token, created = Token.objects.get_or_create(user=user)
    return token
