import pytest
from django.core.urlresolvers import reverse

from wunderhabit import views
from wunderhabit import default
from .utils import get_user

from .utils import mock_messages
from wunderlist.tests.utils import mock_wunderlist_api
from wh_habitica.tests.utils import mock_habitica_api


@pytest.mark.usefixtures('mock_messages', 'mock_wunderlist_api', 'mock_habitica_api')
@pytest.mark.django_db
def test_successfully_authenticated(rf):
    request = rf.get(reverse('test_authentication'))
    request.user = get_user()
    response = views.test_authentication(request)
    assert request._messages.messages[0] == default.MESSAGE_AUTH_SUCCESS
    assert response.url == reverse('dashboard')
