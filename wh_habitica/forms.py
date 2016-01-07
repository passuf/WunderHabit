import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from . import default
from .models import Habitica
from .api import HabiticaApi

logger = logging.getLogger('wunderhabit')


class AuthForm(forms.ModelForm):
    """
    Form to enter and validate the Habitica authentication credentials.
    """
    AUTH_ERROR = _('Could not authenticate to Habitica. Please check the User '
                   'ID and the API Token.')
    HABITICA_ERROR = _('Something went wrong while loading Habitica user data.'
                       ' Please try again or contact the admin.')

    class Meta:
        model = Habitica
        fields = ['user_id', 'api_token']

    def clean(self):
        cleaned_data = super(AuthForm, self).clean()

        api = HabiticaApi(cleaned_data['user_id'], cleaned_data['api_token'])

        try:
            user_details = api.get_user_details()
        except Exception:
            logger.exception('Could not load Habitica user details.')
            raise forms.ValidationError(self.AUTH_ERROR)

        # Validate authentication
        if not user_details or cleaned_data['user_id'] != user_details[default.JSON_ID]:
            raise forms.ValidationError(self.AUTH_ERROR)

        # Get user details
        try:
            self.instance.name = user_details[default.JSON_NAME]
            self.instance.email = user_details[default.JSON_EMAIL]
        except ValueError:
            logger.exception('Could not get user details: %s', str(user_details))
            raise forms.ValidationError(self.HABITICA_ERROR)

        return cleaned_data
