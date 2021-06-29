from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def signin(user: User):
    # delete old token
    try:
        user.auth_token.delete()
    except User.auth_token.RelatedObjectDoesNotExist:
        pass

    # create new one
    token, created = Token.objects.get_or_create(user=user)
    return token
