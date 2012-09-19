from django.conf.urls.defaults import patterns, url
from bcfg2_views import *


urlpatterns = patterns('',
    url(r'^ups_property$', BCFG2UPSProperty.as_view(), name='bcfg2-machines-ups'),
)

