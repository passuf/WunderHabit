import logging

from wh_habitica.api import HabiticaApi


logging.disable(logging.CRITICAL)


def test_server_status():
    api = HabiticaApi(user_id=-1, api_token='invalid')
    status = api.get_status()
    assert status is True or status is False
