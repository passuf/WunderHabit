import habitica as hlib
from . import default


class HabiticaApi(hlib.api.Habitica):
    def __init__(self, user_id, api_token):
        headers = {default.AUTH_HEADER_CLIENT: user_id,
                   default.AUTH_HEADER_TOKEN: api_token}
        super(HabiticaApi, self).__init__(headers)

    def status(self):
        """
        Returns the Habitica server status.
        """

        return self.server()[default.JSON_STATUS] == default.JSON_UP

    def get_user(self):
        """
        Returns the full user object.
        """
        return self.user()

    def post_task(self, task_id, up=True):
        """
        Up- or down-scores a task specified by the task_id.
        """

        if up:
            score = default.JSON_UP
        else:
            score = default.JSON_DOWN

        return self.user.tasks(_id=task_id, _direction=score, _method='post')

    def test_auth(self):
        """
        Tests whether the authentication credentials work or not.
        """

        user = self.get_user()
        if user:
            return True
        else:
            return False
