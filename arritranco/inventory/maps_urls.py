from django.conf.urls import patterns, url
from maps_views import *


urlpatterns = patterns('',
    url(r'^active-machines$', MapsActiveMachinesProperty.as_view(), name='maps-active-machines'),
)

