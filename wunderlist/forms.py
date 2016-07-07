from django import forms
from django.utils.crypto import get_random_string

from .models import Connection
from .api import WunderlistApi


class AddConnectionForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(AddConnectionForm, self).__init__(*args, **kwargs)
        self.user = user

        # Prepare WunderList lists
        self.api = WunderlistApi(user.wunderlist.api_token)
        choices, self.connected = self.api.get_list_choices()
        self.choices = [('', 'empty')] + choices
        self.fields['list_id'].choices = self.choices

        # Prepare Habitica habits
        self.habitica_api = user.habitica.get_api()
        habit_choices, self.habitica_connected = self.habitica_api.get_habits_list_choices()
        self.habit_choices = [('', 'empty')] + habit_choices
        self.fields['habit_id'].choices = self.habit_choices

    list_id = forms.ChoiceField(choices=[], label='')
    habit_id = forms.ChoiceField(choices=[], label='')

    def save(self):

        list_id = self.cleaned_data['list_id']
        habit_id = self.cleaned_data['habit_id']

        list_title = ''
        for choice in self.choices:
            if list_id == str(choice[0]):
                list_title = choice[1]
                break

        habit_title = ''
        for choice in self.habit_choices:
            if habit_id == str(choice[0]):
                habit_title = choice[1]
                break

        connection = Connection.objects.create(
            list_id=list_id,
            list_title=list_title,
            habit_id=habit_id,
            habit_title=habit_title,
            token=get_random_string(32),
            owner=self.user,
        )

        webhook = connection.create_webhook()

        if not webhook:
            connection.delete()
            return None

        return connection
