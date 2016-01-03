from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Sum

from .decorators import is_authenticated
from wunderlist.models import Connection
from wunderlist.decorators import has_wunderlist
from habitica.decorators import has_habitica
from wunderlist.forms import AddConnectionForm


def index(request):
    user = request.user
    if user.is_authenticated() and hasattr(user, 'wunderlist'):
        return redirect('dashboard')
    return render(request, 'wunderhabit/index.html')


@login_required
@has_wunderlist
@has_habitica
def dashboard(request):
    user = request.user
    connections = Connection.objects.filter(owner=user, is_active=True).order_by('list_title')
    form = AddConnectionForm(user)
    if not form.connected:
        return test_authentication(request)

    # Load statistics for superuser
    total_users = 0
    total_connections = 0
    tasks_completed = 0
    if user.is_superuser:
        total_users = User.objects.filter(is_active=True).count()
        total_connections = Connection.objects.filter(is_active=True).count()
        tasks_completed = Connection.objects.aggregate(Sum('tasks_completed'))[
            'tasks_completed__sum']

    return render(request, 'wunderhabit/dashboard.html', {
        'connections': connections,
        'form': form,
        'total_users': total_users,
        'total_connections': total_connections,
        'tasks_completed': tasks_completed,
    })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, _('Successfully logged out.'))
    return redirect('index')


@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        # Delete webhooks and Wunderlist token
        if hasattr(user, 'wunderlist'):
            for connection in user.connections.all():
                connection.deactivate()
            user.wunderlist.delete()

        # Delete Habitica token
        if hasattr(user, 'habitica'):
            user.habitica.delete()

        # Logout user
        logout(request)

        # Delete the user
        user.delete()

        messages.success(request, _('Your account has successfully been deleted.'))

        return redirect('index')

    return render(request, 'wunderhabit/delete_account.html')


@login_required
@has_wunderlist
@has_habitica
def add_connection(request):
    user = request.user

    if request.method == 'POST':
        form = AddConnectionForm(user, request.POST)
        if form.is_valid():
            connection = form.save()
            if connection:
                messages.success(request, _('Created new Connection!'))
            return redirect('index')

    messages.error(request, _('Could not create Connection.'))
    return redirect('dashboard')


@login_required
@has_wunderlist
@has_habitica
def delete_connection(request, connection_id):
    user = request.user

    connection = get_object_or_404(Connection, id=connection_id, owner=user, is_active=True)
    connection.deactivate()

    messages.success(request, _('Deleted the Connection!'))
    return redirect('index')


@login_required
@has_wunderlist
@has_habitica
@is_authenticated
def test_authentication(request):
    messages.success(request, _('Successfully connected with Wunderlist and Habitica.'))
    return redirect('dashboard')
