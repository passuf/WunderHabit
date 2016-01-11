
"""
Wunderlist API Authentication
"""

AUTH_URL = 'https://www.wunderlist.com/oauth/authorize?client_id={client_id}&redirect_uri={url}&state={state}'
AUTH_POST = 'https://www.wunderlist.com/oauth/access_token'
AUTH_POST_CLIENT = 'client_id'
AUTH_POST_SECRET = 'client_secret'
AUTH_POST_CODE = 'code'
AUTH_POST_TOKEN = 'access_token'

AUTH_HEADER_CLIENT = 'X-Client-ID'
AUTH_HEADER_TOKEN = 'X-Access-Token'


"""
Wunderlist API URLS
"""

GET_USER = 'https://a.wunderlist.com/api/v1/user'
GET_LISTS = 'https://a.wunderlist.com/api/v1/lists'
GET_WEBHOOKS = 'https://a.wunderlist.com/api/v1/webhooks?list_id={list_id}'
POST_WEBHOOK = 'https://a.wunderlist.com/api/v1/webhooks'
DELETE_WEBHOOK = 'https://a.wunderlist.com/api/v1/webhooks/{id}'


"""
Wunderlist API JSON
"""

JSON_ID = 'id'
JSON_USER_ID = 'user_id'
JSON_NAME = 'name'
JSON_EMAIL = 'email'
JSON_CREATED_AT = 'created_at'
JSON_REVISION = 'revision'
JSON_LIST_ID = 'list_id'
JSON_URL = 'url'
JSON_PROCESSOR_TYPE = 'processor_type'
JSON_CONFIGURATION = 'configuration'
JSON_SUBJECT = 'subject'
JSON_TYPE = 'type'
JSON_OPERATION = 'operation'
JSON_BEFORE = 'before'
JSON_AFTER = 'after'
JSON_COMPLETED = 'completed'
JSON_TITLE = 'title'

OPERATION_CREATE = 'create'
OPERATION_UPDATE = 'update'

SUBJECT_TASK = 'task'
SUBJECT_SUBTASK = 'subtask'
SUBJECT_LIST = 'list'
