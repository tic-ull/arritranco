from django.conf.urls import patterns, url
from bcfg2_views import *
from inventory.api_views import MachinesNutEpoLevel


urlpatterns = patterns('',
    url(r'^nut$', MachinesNutEpoLevel.as_view(), name='bcfg2-machines-nut'),
)

