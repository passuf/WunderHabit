from django import forms
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from .models import Connection
from .api import WunderlistApi


class AddConnectionForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddConnectionForm, self).__init__(*args, **kwargs)
        self.user = user
        self.api = WunderlistApi(user.wunderlist.api_token)
        choices, self.connected = self.api.get_list_choices()
        self.choices = [('', 'empty')] + choices
        self.fields['list_id'].choices = self.choices

    list_id = forms.ChoiceField(choices=[], label='')
    habit = forms.CharField(max_length=255, min_length=1, initial='productivity')

    def save(self):

        list_id = self.cleaned_data['list_id']
        habit = self.cleaned_data['habit']

        list_title = ''
        for choice in self.choices:
            if list_id == str(choice[0]):
                list_title = choice[1]
                break

        connection = Connection.objects.create(
            list_id=list_id,
            list_title=list_title,
            habit=habit,
            token=get_random_string(32),
            owner=self.user,
        )

        webhook = connection.create_webhook()

        if not webhook:
            connection.delete()
            return None

        return connection
