from django.conf.urls import url

from . import views

app_name = 'list_app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^edit/(P?<token>.{8})$', views.edit_listing, name='edit'),
    url(r'^(?P<pk>[0-9]+)/contact$', views.contact, name='contact'),
    url(r'^new/$', views.new, name='new'),
]