from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse

from wh_habitica.api import HabiticaApi
from .api import WunderlistApi
from . import default


class Wunderlist(models.Model):
    """
    Wunderlist API Endpoint
    """

    user_id = models.IntegerField(_('User ID'))
    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('Email'))
    api_token = models.CharField(_('API Token'), max_length=255)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='wunderlist')

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)

    def get_api(self):
        """
        Returns the Wunderlist API object.
        """

        return WunderlistApi(self.api_token)


class Connection(models.Model):
    """
    Connects a Wunderlist list with a Habitica habit.
    """

    list_id = models.IntegerField(_('List ID'))
    list_title = models.CharField(_('List Title'), max_length=255, blank=True)
    webhook_id = models.IntegerField(_('Webhook ID'), default=-1, blank=True)
    #habit = models.CharField(_('Habit'), max_length=255, blank=True, null=True)
    habit_id = models.CharField(_('Habit ID'), max_length=255, blank=True, null=True)
    habit_title = models.CharField(_('Habit Title'), max_length=255, blank=True, null=True)
    token = models.CharField(_('Token'), max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='connections', blank=True, null=True)
    tasks_completed = models.IntegerField(_('Tasks completed'), default=0)
    last_upscored = models.DateTimeField(_('Last Up-Scored'), default=None, blank=True, null=True)
    is_active = models.BooleanField(_('Is active'), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now=True)

    @property
    def webhook_url(self):
        """
        Returns the absolute URL which is callable by a webhook.
        """

        return settings.WEBHOOK_BASE_URL + reverse('wunderlist:webhook', kwargs={'hook_id': self.token})

    def score_up(self):
        api = HabiticaApi(self.owner.habitica.user_id, self.owner.habitica.api_token)
        self.tasks_completed += 1
        self.last_upscored = timezone.now()
        self.save()
        return api.post_task(self.habit_id)

    def create_webhook(self):
        """
        Sends a request to Wunderlist to create a webhook and stores its id.
        """

        api = WunderlistApi(self.owner.wunderlist.api_token)
        webhook = api.create_webhook(self.list_id, self.webhook_url)
        if webhook:
            self.webhook_id = webhook[default.JSON_ID]
            self.save()
        return webhook

    def delete_webhook(self):
        """
        Sends a request to Wunderlist to delete the webhook.
        """

        if self.webhook_id < 0:
            return None

        api = WunderlistApi(self.owner.wunderlist.api_token)
        return api.delete_webhook(self.webhook_id)

    def deactivate(self):
        """
        Deletes the webhook and and anonymizes the connection such that the number of completed tasks does not get lost.
        """

        self.delete_webhook()
        self.list_title = ''
        self.habit = ''
        self.owner = None
        self.is_active = False
        self.save()

    def delete(self, *args, **kwargs):
        """
        Overrides the delete method to delete the webhook first.
        """

        # Delete the webhook
        print(self.delete_webhook())

        # Delete the connection
        super(Connection, self).delete(*args, **kwargs)
