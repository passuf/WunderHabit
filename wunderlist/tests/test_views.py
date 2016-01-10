import json

import pytest
from django.core.urlresolvers import reverse
from django.http import Http404

from wunderlist import default
from wunderlist.factories import ConnectionFactory
from wunderlist.views import webhook
from wunderhabit.factories import UserFactory


USER_DICT = dict(username='tester', email='foo@bar.com')
INVALID_HOOK_TOKEN = '0000aUZ01eJYBhsIIVZotvc0dY9h0000'


def get_invalid_webhook_body():
    return {
        default.JSON_OPERATION: default.OPERATION_CREATE,
        'no_user_id': -1,
        default.JSON_SUBJECT: {
            'no_type': 'type missing'
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
    connection = ConnectionFactory.create()
    owner = UserFactory.create()
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
