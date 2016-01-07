from django.conf.urls import include, url
from django.contrib import admin

from . import views
from wunderlist import urls as wunderlist_urls
from wh_habitica import urls as habitica_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^account/delete/$', views.delete_account, name='delete_account'),
    url(r'^account/test/$', views.test_authentication, name='test_authentication'),
    url(r'^add/$', views.add_connection, name='add'),
    url(r'^delete/(?P<connection_id>\d+)/$', views.delete_connection, name='delete'),

    url(r'^habitica/', include(habitica_urls, namespace='habitica')),
    url(r'^wunderlist/', include(wunderlist_urls, namespace='wunderlist')),
]
