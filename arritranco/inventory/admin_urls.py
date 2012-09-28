from django.conf.urls.defaults import patterns, include, url

from inventory.admin_views import ActiveMachinesView, UpdateListView

urlpatterns = patterns('',
    url(r'^active-machines/$', ActiveMachinesView.as_view(), name="active-machines"),
    url(r'^update-list/$', UpdateListView.as_view(), name="update-list"),
)

