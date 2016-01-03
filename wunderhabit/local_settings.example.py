import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'some secret key'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Base URL of the site
BASE_URL = 'https://your-site.com'

# Base URL for the webhooks
WEBHOOK_BASE_URL = 'https://your-webhook-site.com'

# The Client ID you received from Wunderlist when you registered your application.
WUNDERLIST_CLIENT_ID = ''
WUNDERLIST_CLIENT_SECRET = ''


# Email Settings
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your_api_key'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

