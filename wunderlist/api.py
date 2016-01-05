import requests
from django.conf import settings

from . import default


class WunderlistApi:
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {default.AUTH_HEADER_CLIENT: settings.WUNDERLIST_CLIENT_ID,
                        default.AUTH_HEADER_TOKEN: api_token}

    @staticmethod
    def request_token(code):
        r = requests.post(default.AUTH_POST, json={
            default.AUTH_POST_CLIENT: settings.WUNDERLIST_CLIENT_ID,
            default.AUTH_POST_SECRET: settings.WUNDERLIST_CLIENT_SECRET,
            default.AUTH_POST_CODE: code,
        })

        if not r or not r.status_code == 200:
            return None

        try:
            token = r.json()
        except ValueError:
            return None

        return token.get(default.AUTH_POST_TOKEN, None)

    def get_user(self):
        r = requests.get(default.GET_USER, headers=self.headers)

        if not r or not r.status_code == 200:
            return None

        try:
            user = r.json()
        except ValueError:
            return None

        if all(k in user for k in (default.JSON_ID, default.JSON_EMAIL, default.JSON_NAME)):
            return user
        else:
            return None

    def get_lists(self):
        r = requests.get(default.GET_LISTS, headers=self.headers)

        if not r or not r.status_code == 200:
            return None

        try:
            lists = r.json()
        except ValueError:
            return None

        return lists

    def get_list_choices(self):
        """
        Returns a tuple with the list (possibly empty) and a boolean indicating the success of the api request.
        """

        lists = self.get_lists()

        if lists is None:
            return [], False

        choices = [(l['id'], l['title']) for l in lists]
        choices = sorted(choices, key=lambda x: x[1])
        return choices, True

    def get_webhooks(self, list_id):
        r = requests.get(default.GET_WEBHOOKS.format(list_id=list_id), headers=self.headers)

        if not r or not r.status_code == 200:
            return None

        try:
            webhooks = r.json()
        except ValueError:
            return None

        return webhooks

    def create_webhook(self, list_id, url):
        r = requests.post(default.POST_WEBHOOK, headers=self.headers, json={
            default.JSON_LIST_ID: list_id,
            default.JSON_URL: url,
            default.JSON_PROCESSOR_TYPE: 'generic',
            default.JSON_CONFIGURATION: '',
        })

        if not r or not r.status_code == 201:
            return None

        try:
            webhook = r.json()
        except ValueError:
            return None

        return webhook

    def delete_webhook(self, hook_id):
        r = requests.delete(default.DELETE_WEBHOOK.format(id=hook_id), headers=self.headers)

        if not r or not r.status_code == 204:
            return None

        return True

    def test_auth(self):
        user = self.get_user()
        if user:
            return True
        else:
            return False
