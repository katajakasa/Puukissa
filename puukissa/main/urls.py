# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'puukissa.main.views',
    url(r'^$', 'index', name="index"),
    url(r'^lessons/', 'lessons', name="lessons"),
    url(r'^profile/', 'profile', name="profile"),
    url(r'^top/', 'top', name="top"),
    url(r'^perform/(?P<lesson_id>\d+)/', 'perform', name="perform"),
    url(r'^json/execute/', 'json_execute', name="json_execute"),
    url(r'^json/turnin/', 'json_turnin', name="json_turnin"),
    url(r'^json/hint/', 'json_hint', name="json_hint"),
    url(r'^login/', 'm_login', name="login"),
    url(r'^logout/', 'm_logout', name="logout"),
)