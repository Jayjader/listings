from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit_listing, name='edit'),
    url(r'^(?P<pk>[0-9]+)/contact$', views.contact, name='contact'),
    url(r'^new/$', views.create_listing, name='new'),
]