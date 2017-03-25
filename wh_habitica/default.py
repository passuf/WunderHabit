
"""
Habitica API
These constants are only used for mock testing the API.
"""


AUTH_URL = 'url'
AUTH_HEADER_CLIENT = 'x-api-user'
AUTH_HEADER_TOKEN = 'x-api-key'

API_HOST = 'https://habitica.com'
API_BASE_URL = API_HOST + '/api/v3'

GET_STATUS = API_BASE_URL + '/status'
GET_USER = API_BASE_URL + '/user'
GET_USER_ANONYMIZED = API_BASE_URL + '/user/anonymized'
POST_TASK = API_BASE_URL + '/tasks/user/{id}/{direction}'

JSON_STATUS = 'status'
JSON_UP = 'up'
JSON_DOWN = 'down'
JSON_ID = 'id'
JSON_DELTA = 'delta'
JSON_BUFFS = 'buffs'
JSON_AUTH = 'auth'
JSON_LOCAL = 'local'
JSON_FACEBOOK = 'facebook'
JSON_GOOGLE = 'google'
JSON_GOOGLE_EMAILS = 'emails'
JSON_DISPLAY_NAME = 'displayName'
JSON_FORMAT_JSON = '_json'
JSON_USERNAME = 'username'
JSON_EMAIL = 'email'
JSON_NAME = 'name'
JSON_VALUE = 'value'
JSON_TYPE = 'type'
