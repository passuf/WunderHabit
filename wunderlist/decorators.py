from django.shortcuts import redirect


def has_wunderlist(view_func):
    """
    Checks if the current user is connected to Wunderlist.
    If not, the user is redirected to the Wunderlist connect page.
    """

    def _wrapped_view_func(request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'wunderlist'):
            return redirect('index')
        if not user.wunderlist.api_token:
            return redirect('index')
        if not user.wunderlist.user_id:
            return redirect('index')
        if not user.wunderlist.email:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
