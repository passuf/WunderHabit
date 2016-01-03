from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^auth/check/$', views.auth_check, name='auth_check'),
    url(r'^reconnect/$', views.reconnect, name='reconnect'),
    url(r'^webhook/(?P<hook_id>[\w{}.-]{32})/$', views.webhook, name='webhook'),
    url(r'^webhooks/check/$', views.check_webhooks, name='check_webhooks'),
]
