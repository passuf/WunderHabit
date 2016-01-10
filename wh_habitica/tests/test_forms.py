import json
import logging
import pytest
import responses

from wh_habitica import default
from wh_habitica.forms import AuthForm
from wunderhabit.factories import UserFactory


logging.disable(logging.CRITICAL)

USER_DICT = dict(username='tester', email='foo@bar.com')


def get_user_callback(request):
    if request.headers.get(default.AUTH_HEADER_TOKEN) != 'correct':
        return (401, {}, {
            "err": "No user found."
        })

    if request.headers.get(default.AUTH_HEADER_CLIENT) == 'facebook_auth':
        # Facebook user can chose to expose a bunch of things, we'll test for name & email:
        # https://github.com/HabitRPG/habitrpg/blob/44dd6674d18906047c452b7375b522e579c489e3/website/src/models/user.js#L504
        user = {default.JSON_FORMAT_JSON: dict(
            name=USER_DICT['username'], email=USER_DICT['email']
        )}
        return (200, {}, json.dumps({
            'id': request.headers.get(default.AUTH_HEADER_CLIENT),
            'auth': {
                'local': {},
                'facebook': user, }}))

    elif request.headers.get(default.AUTH_HEADER_CLIENT) == 'facebook_fail?':
        return (200, {}, json.dumps({
            'id': request.headers.get(default.AUTH_HEADER_CLIENT),
            'auth': {
                'local': {},
                'facebook': USER_DICT, }}))

    return (200, {}, json.dumps({
        'id': request.headers.get(default.AUTH_HEADER_CLIENT),
        'auth': {
            'facebook': {},
            'local': USER_DICT, }}))


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
def test_unsupported_field_change(get_user):
    # all good on our end, but server now also supports twitter users
    res = AuthForm(data=dict(user_id='facebook_fail?', api_token='correct'))
    assert not res.is_valid()
    assert res.errors == {'__all__': [AuthForm.HABITICA_ERROR]}


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
    assert res.instance.name == 'tester'
    assert res.instance.email == 'foo@bar.com'

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
    assert res.instance.name == 'tester'
    assert res.instance.email == 'foo@bar.com'

    # assert save returned valid object for saving
    owner = UserFactory.create()
    instance = res.save(commit=False)
    instance.owner = owner
    instance.save()
