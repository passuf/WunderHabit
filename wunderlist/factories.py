import factory

from django.utils.crypto import get_random_string

from .models import Connection, Wunderlist
from wunderhabit.factories import UserFactory


class WunderlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wunderlist

    user_id = factory.Sequence(lambda n: "%d" % n)
    name = 'John'
    email = 'john@doe.com'
    api_token = get_random_string(32)
    owner = factory.SubFactory(UserFactory)


class ConnectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Connection

    list_id = 42
    token = get_random_string(32)
