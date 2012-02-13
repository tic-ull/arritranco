from django.conf.urls.defaults import patterns, url
from views import hosts, hosts_ext_info, backup_checks, generic_checks


urlpatterns = patterns('',
    url(r'^hosts.cfg$', hosts, name='hosts'),
    url(r'^hosts_ext_info.cfg$', hosts_ext_info, name='hosts_ext_info'),
    url(r'^backup_checks.cfg$', backup_checks, name='backup_checks'),
    url(r'^disk_checks.cfg$', generic_checks, {'template':'nagios/disk_checks.cfg'}, name='disk_checks'),
    url(r'^mem_checks.cfg$', generic_checks, {'template':'nagios/mem_checks.cfg'}, name='mem_checks'),
    url(r'^load_checks.cfg$', generic_checks, {'template':'nagios/load_checks.cfg'}, name='load_checks'),
)
