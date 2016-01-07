from django import forms
from django.utils.translation import ugettext_lazy as _

from . import default
from .models import Habitica
from .api import HabiticaApi


class AuthForm(forms.ModelForm):
    """
    Form to enter and validate the Habitica authentication credentials.
    """

    class Meta:
        model = Habitica
        fields = ['user_id', 'api_token']

    def clean(self):
        cleaned_data = super(AuthForm, self).clean()

        api = HabiticaApi(cleaned_data['user_id'], cleaned_data['api_token'])

        try:
            user = api.get_user()
            user_info = user[default.JSON_AUTH][default.JSON_LOCAL]
            self.instance.name = user_info[default.JSON_USERNAME]
            self.instance.email = user_info[default.JSON_EMAIL]
        except Exception:
            raise forms.ValidationError(
                _('Could not authenticate to Habitica. Please check the User ID and the API Token.'))

        return cleaned_data
