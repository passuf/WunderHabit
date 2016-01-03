from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.auth, name='index'),
    url(r'^reconnect/$', views.reconnect, name='reconnect'),
]
