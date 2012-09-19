from django.conf.urls.defaults import patterns, url
from views import hosts, hosts_ext_info, backup_checks, get_checks, refresh_nagios_status


urlpatterns = patterns('',
    url(r'^gethosts$', hosts, name='hosts'),
    url(r'^refresh_nagios$', refresh_nagios_status, name='refresh_nagios_status'),
    url(r'^gethosts/extinfo$', hosts_ext_info, name='hosts_ext_info'),
    url(r'^backup_checks.cfg$', backup_checks, name='backup_checks_old'),
#    url(r'^load_checks.cfg$', generic_checks, {'template':'nagios/load_checks.cfg'}, name='load_checks'),
    url(r'^getchecks/backup$', backup_checks, name='backup_checks'),
    url(r'^getchecks/(?P<name>[-\w]+)$', get_checks, name='get_checks'),
)
