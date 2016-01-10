import factory

from django.utils.crypto import get_random_string

from .models import Connection, Wunderlist


class WunderlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wunderlist

    user_id = 42
    name = 'John'
    email = 'john@doe.com'
    api_token = get_random_string(32)


class ConnectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Connection

    list_id = 42
    token = get_random_string(32)
