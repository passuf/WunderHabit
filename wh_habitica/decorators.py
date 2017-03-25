from django.shortcuts import redirect


def has_habitica(view_func):
    """
    Checks if the current user is connected to Habitica.
    If not, the user is redirected to the Habitica connect page.
    """

    def _wrapped_view_func(request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'habitica'):
            return redirect('habitica:index')
        if not user.habitica.api_token:
            return redirect('habitica:index')
        if not user.habitica.user_id:
            return redirect('habitica:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
