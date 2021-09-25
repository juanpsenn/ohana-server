import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Faker("name", locale="es_ES")
    password = factory.Faker("password")
    email = factory.Faker("email")
