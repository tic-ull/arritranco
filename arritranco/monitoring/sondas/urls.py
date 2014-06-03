from django.conf.urls import patterns, url
from views import NrpeCfg, NrpeHosts


urlpatterns = patterns('',
    url(r'^getchecks$', NrpeCfg.as_view(), name='nrpe'),
    url(r'^gethosts', NrpeHosts.as_view(), name='nrpehosts'),
)
