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
            raise forms.ValidationError(
                    _('Could not authenticate to Habitica. Please check the User ID and the API Token.'))

        # Validate authentication
        if not user_details or cleaned_data['user_id'] != user_details[default.JSON_ID]:
            raise forms.ValidationError(
                _('Could not authenticate to Habitica. Please check the User ID and the API Token.'))

        # Get user details
        try:
            self.instance.name = user_details[default.JSON_NAME]
            self.instance.email = user_details[default.JSON_EMAIL]
        except ValueError:
            logger.exception('Could not get user details: ' + str(user_details))
            raise forms.ValidationError(
                    _('Something went wrong while connecting with Habitica. Please try again or contact the admin.'))

        return cleaned_data
