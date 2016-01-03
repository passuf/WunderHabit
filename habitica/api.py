import requests
import urllib

from . import default


class HabiticaApi:
    def __init__(self, user_id, api_token):
        self.user_id = user_id
        self.api_token = api_token
        self.headers = {default.AUTH_HEADER_CLIENT: user_id,
                        default.AUTH_HEADER_TOKEN: api_token}

    @staticmethod
    def status():
        """
        Returns the Habitica server status.
        """

        r = requests.get(default.GET_STATUS)

        if not r or not r.status_code == 200:
            return None

        try:
            status = r.json()
            if status[default.JSON_STATUS] == default.JSON_UP:
                return True
        except Exception:
            return None

        return False

    def get_user(self):
        """
        Returns the full user object.
        """

        r = requests.get(default.GET_USER, headers=self.headers)

        if not r or not r.status_code == 200:
            return None

        try:
            user = r.json()
            user_info = user[default.JSON_AUTH][default.JSON_LOCAL]
            if default.JSON_USERNAME not in user_info or default.JSON_EMAIL not in user_info:
                return None
        except Exception:
            return None

        return user

    def post_task(self, task_id, up=True):
        """
        Up- or down-scores a task specified by the task_id.
        """

        if up:
            score = default.JSON_UP
        else:
            score = default.JSON_DOWN

        r = requests.post(
                default.POST_TASK.format(id=urllib.quote_plus(task_id), direction=score),
                headers=self.headers,
                json={},
        )

        if not r or not r.status_code == 200:
            return None

        try:
            result = r.json()
        except Exception:
            return None

        return result

    def test_auth(self):
        """
        Tests whether the authentication credentials work or not.
        """

        user = self.get_user()
        if user:
            return True
        else:
            return False
