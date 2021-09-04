import factory.django


class ContactInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.ContactInformation"

    name = factory.Faker("name_nonbinary", locale="es_ES")
    phone = factory.Faker("phone_number")
    email = factory.Faker("ascii_free_email", locale="es_ES")


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.Location"

    street = factory.Faker("street_name", locale="es_ES")
    address_line = factory.Faker("street_address", locale="es_ES")
    postal_code = 5000


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "app.Category"

    name = factory.Faker("sentence", nb_words=1)
