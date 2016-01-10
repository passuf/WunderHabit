import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .api import WunderlistApi
from .models import Wunderlist, Connection
from .decorators import has_wunderlist
from . import default


def auth(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'wunderlist'):
        return redirect('dashboard')

    callback_url = request.build_absolute_uri(reverse('wunderlist:auth_check'))
    random_state = get_random_string(length=32)
    request.session['random_state'] = random_state
    return redirect(default.AUTH_URL.format(
            client_id=settings.WUNDERLIST_CLIENT_ID,
            url=callback_url,
            state=random_state
    ))


def auth_check(request):
    # Check if state matches
    if request.session.get('random_state', -1) != request.GET.get('state', -2):
        messages.error(request, _('State not valid'))
        return redirect('index')

    # Get temporary code
    code = request.GET.get('code', -1)

    # Request token
    token = WunderlistApi.request_token(code)

    # Validate token
    if not token:
        messages.error(request, _('No token received'))
        return redirect('index')

    # Request Wunderlist User
    api = WunderlistApi(token)
    wunderlist_user = api.get_user()

    # Validate user
    if not wunderlist_user:
        messages.error(request, _('Invalid user received'))
        return redirect('index')

    # Authenticate the user to Django
    try:
        user = User.objects.get(email=wunderlist_user.get(default.JSON_EMAIL))
    except ObjectDoesNotExist:
        # Create new Django user
        user = User.objects.create(
                username=wunderlist_user.get(default.JSON_EMAIL),
                email=wunderlist_user.get(default.JSON_EMAIL),
                first_name=wunderlist_user.get(default.JSON_NAME),
                is_staff=False,
                is_superuser=False,
        )
        messages.success(request, _('Connected with Wunderlist'))
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    if user and user.is_active:
        login(request, user)
    else:
        messages.error(request, _('This account has been disabled.'))
        return redirect('index')

    # Update or create Wunderlist object and map it to user
    updated_values = {
        'name': wunderlist_user.get(default.JSON_NAME),
        'email': wunderlist_user.get(default.JSON_EMAIL),
        'owner': user,
        'api_token': token,
    }
    Wunderlist.objects.update_or_create(user_id=wunderlist_user.get(default.JSON_ID), defaults=updated_values)

    return redirect('dashboard')


@csrf_exempt
def webhook(request, hook_id):
    connection = get_object_or_404(Connection, token=hook_id)

    if request.method != 'POST':
        return HttpResponse(status=400)

    try:
        data = json.loads(request.body)
        operation = data.get(default.JSON_OPERATION)
        user_id = int(data.get(default.JSON_USER_ID))
        subject = data.get(default.JSON_SUBJECT)
        subject_type = subject.get(default.JSON_TYPE)
    except Exception:
        return HttpResponse(status=400)

    # Check if connection is active
    if not connection.is_active:
        return HttpResponse(status=410)

    # Find Wunderlist user
    try:
        wunderlist = Wunderlist.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return HttpResponse(status=401)

    # Validate user
    user = connection.owner
    if not user or not wunderlist or user != wunderlist.owner:
        return HttpResponse(status=401)

    # Check if user is active
    if not user.is_active:
        return HttpResponse(status=403)

    # Check if a task or subtask has been added to the list
    if operation == default.OPERATION_CREATE:
        # New task has been added to list
        return HttpResponse(status=200)

    # Check if a task has been updated (includes completion)
    if operation == default.OPERATION_UPDATE:
        try:
            before = data.get(default.JSON_BEFORE)
            before_completed = before.get(default.JSON_COMPLETED, False)
            after = data.get(default.JSON_AFTER)
            after_completed = after.get(default.JSON_COMPLETED, False)
        except Exception:
            return HttpResponse(status=400)

        if not before_completed and after_completed:
            if subject_type == default.SUBJECT_TASK:
                # Task has been completed
                connection.score_up()
                return HttpResponse(status=200)

            elif subject_type == default.SUBJECT_SUBTASK:
                # Subtask has been completed
                connection.score_up()
                return HttpResponse(status=200)

    return HttpResponse(status=400)


@login_required
@has_wunderlist
def reconnect(request):
    request.user.wunderlist.delete()
    logout(request)
    return redirect('wunderlist:auth')


@login_required
@user_passes_test(lambda u: u.is_staff)
@has_wunderlist
def check_webhooks(request):
    user = request.user

    if not hasattr(user, 'wunderlist'):
        return render(request, 'wunderlist/check_webhooks.html')

    api = WunderlistApi(user.wunderlist.api_token)
    lists = api.get_lists()

    if lists is None:
        messages.error(request, _('Could not get lists from Wunderlist. Please try to reconnect.'))
        return redirect('index')

    webhooks = []
    for l in lists:
        webhooks.extend(api.get_webhooks(l[default.JSON_ID]))

    return render(request, 'wunderlist/check_webhooks.html', {'lists': lists, 'webhooks': webhooks})
