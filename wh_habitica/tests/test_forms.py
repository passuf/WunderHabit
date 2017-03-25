import json
import logging
import pytest
import responses

from wh_habitica import default
from wh_habitica.forms import AuthForm
from wunderhabit.factories import UserFactory
from wh_habitica.tests import utils

logging.disable(logging.CRITICAL)

USER_DICT = dict(username='tester', email='foo@bar.com')


def get_user_callback(request):
    if request.headers.get(default.AUTH_HEADER_TOKEN) != 'correct':
        return (401, {}, {
            "err": "No user found."
        })

    if request.headers.get(default.AUTH_HEADER_CLIENT) == 'facebook_auth':
        data = utils.API_USER_FACEBOOK
        data[default.JSON_ID] = request.headers.get(default.AUTH_HEADER_CLIENT)

    elif request.headers.get(default.AUTH_HEADER_CLIENT) == 'google_auth':
        data = utils.API_USER_FACEBOOK
        data[default.JSON_ID] = request.headers.get(default.AUTH_HEADER_CLIENT)

    elif request.headers.get(default.AUTH_HEADER_CLIENT) == 'auth_provider_fail?':
        data = utils.API_USER_INVALID
        data[default.JSON_ID] = request.headers.get(default.AUTH_HEADER_CLIENT)

    else:
        # Local auth provider
        data = utils.API_USER
        data[default.JSON_ID] = request.headers.get(default.AUTH_HEADER_CLIENT)

    return 200, {}, json.dumps({'data': data})


@pytest.fixture
def get_user():
    responses.add_callback(
        responses.GET, default.GET_USER,
        callback=get_user_callback,
        content_type='application/json',
    )


@pytest.fixture
def api_error():
    responses.add(
        responses.GET, default.GET_USER,
        body=Exception('Some Habitica API Error occurred!'),
        content_type='application/json',
    )


@responses.activate
def test_auth_error(get_user):
    # bad api auth result
    res = AuthForm(data=dict(user_id='foo', api_token='baz'))
    assert not res.is_valid()
    assert res.errors == {'__all__': [AuthForm.AUTH_ERROR]}


@responses.activate
def test_no_user_details(get_user):
    # We still want to accept users which do not expose further user details
    res = AuthForm(data=dict(user_id='auth_provider_fail?', api_token='correct'))
    assert res.is_valid()


@responses.activate
def test_other_api_error(api_error):
    # all good on our end, server returned error
    res = AuthForm(data=dict(user_id='raise_error', api_token='raise_error'))
    assert not res.is_valid()
    assert res.errors == {'__all__': [AuthForm.AUTH_ERROR]}


@responses.activate
@pytest.mark.django_db
def test_local_auth_user(get_user):
    # good local api auth result
    res = AuthForm(data=dict(user_id='local_auth', api_token='correct'))
    assert res.is_valid(), 'form errors: %s' % res.errors
    assert res.instance.name == utils.LOCAL_NAME
    assert res.instance.email == utils.USER_EMAIL

    # assert save returned valid object for saving
    owner = UserFactory.create()
    instance = res.save(commit=False)
    instance.owner = owner
    instance.save()


@responses.activate
@pytest.mark.django_db
def test_facebook_auth_user(get_user):
    # good local api auth result
    res = AuthForm(data=dict(user_id='facebook_auth', api_token='correct'))
    assert res.is_valid(), 'form errors: %s' % res.errors

    # assert save returned valid object for saving
    owner = UserFactory.create()
    instance = res.save(commit=False)
    instance.owner = owner
    instance.save()


@responses.activate
@pytest.mark.django_db
def test_google_auth_user(get_user):
    # good local api auth result
    res = AuthForm(data=dict(user_id='google_auth', api_token='correct'))
    assert res.is_valid(), 'form errors: %s' % res.errors

    # assert save returned valid object for saving
    owner = UserFactory.create()
    instance = res.save(commit=False)
    instance.owner = owner
    instance.save()
