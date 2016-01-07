from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .api import HabiticaApi


class Habitica(models.Model):
    """
    Habitica API Endpoint
    """

    user_id = models.CharField(_('User ID'), max_length=255, blank=True)
    name = models.CharField(_('Name'), max_length=255, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    api_token = models.CharField(_('API Token'), max_length=255, blank=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='habitica')

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)

    def get_api(self):
        """
        Returns the Habitica API object.
        """

        return HabiticaApi(self.user_id, self.api_token)

    class Meta:
        db_table = 'habitica_habitica'
