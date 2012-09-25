from django.conf.urls.defaults import patterns, include, url

from hardware.admin_views import RoomRackView

urlpatterns = patterns('',
    url(r'^room-rack$', RoomRackView.as_view(), name="room-rack-view"),
)

