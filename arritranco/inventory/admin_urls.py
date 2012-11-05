from django.conf.urls.defaults import patterns, include, url

from inventory.admin_views import ActiveMachinesView, UpdateListView, EPOListView

urlpatterns = patterns('',
    url(r'^active-machines/$', ActiveMachinesView.as_view(), name="active-machines"),
    url(r'^update-list/$', UpdateListView.as_view(), name="update-list"),
    url(r'^epo-list/$', EPOListView.as_view(), name="epo-list"),
    url(r'^epo-list/(\w+)/$', EPOListView.as_view(), name="epo-list"),
)

