from django.conf.urls.defaults import patterns, url
from bcfg2_views import *


urlpatterns = patterns('',
    url(r'^ups_property$', MachinesUPSProperty.as_view(), name='bcfg2-machines-ups'),
    url(r'^ups_assoc$', MachinesUPSProperty.as_view(), name='machines-ups-assoc'),
    url(r'^ups_assoc/(?P<up>[01]+)$', MachinesUPSProperty.as_view(), name='machines-ups-assoc-up'),
)

