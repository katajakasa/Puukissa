from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

# Usual urls
urlpatterns = patterns('',
    url(r'^$', include('puukissa.main.urls')),
    url(r'^main/', include('puukissa.main.urls', namespace="main")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^openid/', include('django_openid_auth.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

# Serve media files through static.serve when running in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^content/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
