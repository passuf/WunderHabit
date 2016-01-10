import pytest

from wh_habitica import default

API_STATUS_UP = {default.JSON_STATUS: default.JSON_UP}
LOCAL_NAME = 'John Local'
FACEBOOK_NAME = 'John Facebook'
USER_EMAIL = 'john@doe.com'
API_USER = {
    default.JSON_ID: 42,
    default.JSON_AUTH: {
        default.JSON_LOCAL: {default.JSON_USERNAME: LOCAL_NAME, default.JSON_EMAIL: USER_EMAIL},
    }
}
API_USER_FACEBOOK = {
    default.JSON_ID: 42,
    default.JSON_AUTH: {
        default.JSON_LOCAL: {},
        default.JSON_FACEBOOK: {
            default.JSON_FORMAT_JSON: {default.JSON_NAME: FACEBOOK_NAME, default.JSON_EMAIL: USER_EMAIL},
        }
    }
}
API_TASK = {default.JSON_DELTA: 1}


@pytest.fixture
def mock_habitica_api(monkeypatch):
    monkeypatch.setattr('habitica.api.Habitica.status', lambda x: API_STATUS_UP, raising=False)
    monkeypatch.setattr('habitica.api.Habitica.user', lambda x: API_USER, raising=False)
    monkeypatch.setattr('wh_habitica.api.HabiticaApi.post_task', lambda x, task_id: API_TASK, raising=False)


@pytest.fixture
def mock_habitica_api_facebook(monkeypatch):
    monkeypatch.setattr('habitica.api.Habitica.user', lambda x: API_USER_FACEBOOK, raising=False)
