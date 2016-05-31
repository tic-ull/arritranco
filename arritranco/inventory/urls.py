from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^update_update_date/(?P<machine_id>\d+)$', update_update_date, name="update_update_date"),
    url(r'^get_machine_by_os/(?P<req_os>[\w ]+)/?$', get_up_machines_by_os, name="get_up_machines_by_os"),
)
