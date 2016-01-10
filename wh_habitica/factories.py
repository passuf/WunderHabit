import factory

from django.utils.crypto import get_random_string

from .models import Habitica
from wunderhabit.factories import UserFactory


class HabiticaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habitica

    user_id = factory.Sequence(lambda n: "%d" % n)
    name = 'John'
    email = 'john@doe.com'
    api_token = get_random_string(32)
    owner = factory.SubFactory(UserFactory)
