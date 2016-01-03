from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.translation import ugettext_lazy as _


def is_authenticated(view_func):
    """
    Checks if the current user is authenticated against Wunderlist and Habitica.
    If not, the user is redirected to the index page.
    """

    def _wrapped_view_func(request, *args, **kwargs):
        user = request.user

        if not hasattr(user, 'wunderlist'):
            return redirect('index')

        if not hasattr(user, 'habitica'):
            return redirect('index')

        w_api = user.wunderlist.get_api()
        h_api = user.habitica.get_api()

        # Test Wunderlist
        if not w_api.test_auth():
            user.wunderlist.delete()
            messages.error(request, _('Could not connect to Wunderlist. Please re-connect'))
            logout(request)
            return redirect('index')

        # Test Habitica
        if not h_api.status():
            messages.error(request, _('Habitica servers are currently not responding. Please try again later.'))
            return redirect('dashboard')
        if not h_api.test_auth():
            user.habitica.delete()
            messages.error(request, _('Could not connect to Habitica. Please re-connect.'))
            return redirect('dashboard')

        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
