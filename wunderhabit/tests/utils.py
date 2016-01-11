import pytest

from wunderlist.factories import WunderlistFactory
from wh_habitica.factories import HabiticaFactory


def get_user():
    """
    Returns a user which is connected with wunderlist and habitica.
    """

    wunderlist = WunderlistFactory.create()
    habitica = HabiticaFactory.create()
    habitica.owner = wunderlist.owner
    habitica.save()
    return wunderlist.owner


class MockMessages(object):
    """
    Implements a fallback store for Django messages such that they can be accessed in tests.
    The messages are appended to the request object: request._messages and can be accessed via the messages list.
    """

    def __init__(self):
        self.messages = []

    def add(self, level, message, extra_tags):
        self.messages.append(unicode(message))


@pytest.fixture(autouse=True)
def mock_messages(monkeypatch):
    monkeypatch.setattr('django.http.HttpRequest._messages', MockMessages(), raising=False)
