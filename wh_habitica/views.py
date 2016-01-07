from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .forms import AuthForm
from .decorators import has_habitica
from wunderlist.decorators import has_wunderlist


@login_required
@has_wunderlist
def auth(request):
    """
    Authenticates the user to Habitica.
    """

    user = request.user

    if hasattr(user, 'habitica'):
        return redirect('index')

    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(request.POST)

        if form.is_valid():
            habitica = form.save(commit=False)
            habitica.owner = user
            habitica.save()
            messages.success(request, _('Successfully connected with Habitica.'))
            return redirect('index')

    return render(request, 'habitica/index.html', {'form': form})


@login_required
@has_wunderlist
@has_habitica
def reconnect(request):
    """
    Deletes the Habitica credential and redirects to the authentication site.
    """

    request.user.habitica.delete()
    return redirect('habitica:index')

