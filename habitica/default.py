
"""
Habitica API
"""


AUTH_HEADER_CLIENT = 'x-api-user'
AUTH_HEADER_TOKEN = 'x-api-key'

API_BASE_URL = 'https://habitica.com/api/v2'


GET_STATUS = API_BASE_URL + '/status'

GET_USER = API_BASE_URL + '/user'
GET_USER_ANONYMIZED = API_BASE_URL + '/user/anonymized'

POST_TASK = API_BASE_URL + '/user/tasks/{id}/{direction}'

JSON_STATUS = 'status'
JSON_UP = 'up'
JSON_DOWN = 'down'
JSON_ID = 'id'
JSON_DELTA = 'delta'
JSON_BUFFS = 'buffs'

JSON_AUTH = 'auth'
JSON_LOCAL = 'local'
JSON_USERNAME = 'username'
JSON_EMAIL = 'email'
