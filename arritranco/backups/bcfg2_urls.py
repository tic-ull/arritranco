from django.conf.urls.defaults import patterns, url
from bcfg2_views import *

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = patterns('',
    url(r'^property$', BCFG2BackupProperty.as_view(), name='bcfg2-backup-property'),
)

urlpatterns = format_suffix_patterns(urlpatterns)