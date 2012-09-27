from django.conf.urls.defaults import patterns, include, url

from inventory.admin_views import ActiveMachinesView

urlpatterns = patterns('',
    url(r'^active-machines/$', ActiveMachinesView.as_view(), name="active-machines"),
)

