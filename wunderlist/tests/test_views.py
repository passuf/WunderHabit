import json
import pytest
from django.core.urlresolvers import reverse
from django.http import Http404

from wunderlist import default
from wunderlist.factories import WunderlistFactory, ConnectionFactory
from wunderlist.views import webhook
from wh_habitica.factories import HabiticaFactory
from wh_habitica.tests.utils import mock_habitica_api


USER_DICT = dict(username='tester', email='foo@bar.com')
INVALID_HOOK_TOKEN = '0000aUZ01eJYBhsIIVZotvc0dY9h0000'


def get_user():
    """
    Returns a user which is connected with wunderlist and habitica.
    """
    wunderlist = WunderlistFactory.create()
    habitica = HabiticaFactory.create()
    habitica.owner = wunderlist.owner
    habitica.save()
    return wunderlist.owner


def get_invalid_webhook_body():
    return {
        default.JSON_OPERATION: default.OPERATION_CREATE,
        'no_user_id': -1,
        default.JSON_SUBJECT: {
            'no_type': 'type missing'
        },
    }


def get_valid_webhook_body(
        op=default.OPERATION_UPDATE,
        user_id=-1,
        subject_type=default.SUBJECT_TASK,
        completed_before=False,
        completed_after=True,
):
    return {
        default.JSON_OPERATION: op,
        default.JSON_USER_ID: user_id,
        default.JSON_SUBJECT: {
            default.JSON_TYPE: subject_type
        },
        default.JSON_BEFORE: {
            default.JSON_COMPLETED: completed_before,
        },
        default.JSON_AFTER: {
            default.JSON_COMPLETED: completed_after,
        },
    }


@pytest.mark.django_db
def test_webhook_invalid_token(rf):
    request = rf.post(reverse('wunderlist:webhook', kwargs={'hook_id': INVALID_HOOK_TOKEN}))
    with pytest.raises(Http404):
        response = webhook(request, hook_id=INVALID_HOOK_TOKEN)


@pytest.mark.django_db
def test_webhook_invalid_request_type(rf):
    connection = ConnectionFactory.create()
    request = rf.get(reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}))
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_webhook_invalid_request_body(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_invalid_webhook_body()
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_webhook_inactive_connection(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.is_active = False
    connection.save()

    post_data = get_valid_webhook_body()
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 410


@pytest.mark.django_db
def test_webhook_invalid_wunderlist_user(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_valid_webhook_body(user_id=-1)
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 401


@pytest.mark.django_db
def test_webhook_wrong_user(rf):
    owner = get_user()
    wrong_user = get_user()
    connection = ConnectionFactory.create()
    connection.owner = wrong_user
    connection.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id)
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 401


@pytest.mark.django_db
def test_webhook_inactive_user(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()
    owner.is_active = False
    owner.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id)
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 403


@pytest.mark.django_db
def test_webhook_task_completed(rf, mock_habitica_api):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id)
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_webhook_subtask_completed(rf, mock_habitica_api):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id, subject_type=default.SUBJECT_SUBTASK)
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_webhook_invalid_task_body(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id)
    del post_data[default.JSON_AFTER]
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_webhook_task_created(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id, op=default.OPERATION_CREATE)
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_webhook_unknown_operation(rf):
    owner = get_user()
    connection = ConnectionFactory.create()
    connection.owner = owner
    connection.save()

    post_data = get_valid_webhook_body(user_id=owner.wunderlist.user_id, op='op_unknown')
    request = rf.post(
            reverse('wunderlist:webhook', kwargs={'hook_id': connection.token}),
            json.dumps(post_data),
            content_type="application/json",
    )
    response = webhook(request, hook_id=connection.token)
    assert response.status_code == 400
