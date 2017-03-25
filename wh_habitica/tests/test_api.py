import logging

from wh_habitica import default
from wh_habitica.api import HabiticaApi
from .utils import mock_habitica_api, mock_habitica_api_facebook, mock_habitica_api_google, \
    mock_habitica_api_invalid_provider
from wh_habitica.tests import utils

logging.disable(logging.CRITICAL)


def test_server_status(mock_habitica_api):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    status = api.get_status()
    assert status is True


def test_get_user_details(mock_habitica_api):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    user_details = api.get_user_details()
    assert default.JSON_ID in user_details
    assert default.JSON_NAME in user_details
    assert user_details[default.JSON_NAME] == utils.LOCAL_NAME
    assert default.JSON_EMAIL in user_details
    assert user_details[default.JSON_EMAIL] == utils.USER_EMAIL


def test_get_user_details_facebook(mock_habitica_api_facebook):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    user_details = api.get_user_details()
    assert default.JSON_ID in user_details
    assert default.JSON_NAME in user_details
    assert user_details[default.JSON_NAME] == utils.FACEBOOK_NAME


def test_get_user_details_google(mock_habitica_api_google):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    user_details = api.get_user_details()
    assert default.JSON_ID in user_details
    assert default.JSON_NAME in user_details
    assert user_details[default.JSON_NAME] == utils.GOOGLE_NAME
    assert default.JSON_EMAIL in user_details
    assert user_details[default.JSON_EMAIL] == utils.USER_EMAIL


def test_get_user_details_invalid_provider(mock_habitica_api_invalid_provider):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    user_details = api.get_user_details()
    assert default.JSON_ID in user_details
    assert default.JSON_NAME not in user_details
    assert default.JSON_EMAIL not in user_details


def test_auth_test(mock_habitica_api):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    auth_status = api.test_auth()
    assert auth_status is True


def test_post_task(mock_habitica_api):
    api = HabiticaApi(user_id=-1, api_token='uses_mok')
    response = api.post_task(task_id='test_id')
    assert default.JSON_DELTA in response
