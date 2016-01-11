import pytest

from wunderlist import default


USER_ID = 42
USER_NAME = 'John Wunderlist'
USER_EMAIL = 'john@doe.com'

API_USER = {default.JSON_ID: USER_ID, default.JSON_NAME: USER_NAME, default.JSON_EMAIL: USER_EMAIL}
API_LISTS = [{default.JSON_ID: 1, default.JSON_TITLE: 'List 1'}, {default.JSON_ID: 2, default.JSON_TITLE: 'List 2'}]


@pytest.fixture(autouse=True)
def mock_wunderlist_api(monkeypatch):
    monkeypatch.setattr('wunderlist.api.WunderlistApi.get_user', lambda x: API_USER, raising=False)
    monkeypatch.setattr('wunderlist.api.WunderlistApi.get_lists', lambda x: API_LISTS, raising=False)
    monkeypatch.setattr('wunderlist.api.WunderlistApi.test_auth', lambda x: True, raising=False)
