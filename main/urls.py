from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^%s$' % settings.URL_INFIX, 'main.views.index'),
    url(r'^%sms-getobject/type/(?P<obj_type>[a-zA-Z]+)/tag/(?P<obj_tag>[a-zA-Z0-9_\-]+)/index/(?P<obj_index>[0-9]+)/' % settings.URL_INFIX, 'main.views.get_object'),
    url(r'^%sms-updatestreams/' % settings.URL_INFIX, 'main.views.update_streams'),
    url(r'^%sms-updatechannels/' % settings.URL_INFIX, 'main.views.update_channels'),
    url(r'^%sms-live_now/$' % settings.URL_INFIX, 'main.views.live_now'),
    url(r'^%sview/$' % settings.URL_INFIX, 'main.views.view_streams'),
    url(r'^%sms-admin/' % settings.URL_INFIX, include(admin.site.urls)),
    url(r'^%sedit/(?P<streams_url>[a-zA-Z0-9_\-/]+)$' % settings.URL_INFIX, 'main.views.index'),
    url(r'^%stag/(?P<tag>[a-zA-Z0-9_\-]+/)$' % settings.URL_INFIX, 'main.views.view_tag'),
    url(r'^%s(?P<streams_url>[a-zA-Z0-9_\-/]+)/$' % settings.URL_INFIX, 'main.views.view_streams'),
    
    # Examples:
    # url(r'^$', 'twinstream.views.home', name='home'),
    # url(r'^twinstream/', include('twinstream.foo.urls')),
)
