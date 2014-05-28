from django.conf.urls import patterns, url
from views import NrpeCfg


urlpatterns = patterns('',
    url(r'^getchecks', NrpeCfg.as_view(), name='nrpe'),
)
