from django.conf.urls.defaults import patterns, url
from bcfg2_views import *


urlpatterns = patterns('',
    url(r'^property$', BCFG2BackupProperty.as_view(), name='bcfg2-backup-propery'),
)
