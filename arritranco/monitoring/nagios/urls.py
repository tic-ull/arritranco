from django.conf.urls.defaults import patterns, url
from views import hosts, hosts_ext_info, backup_checks, get_checks


urlpatterns = patterns('',
    url(r'^gethosts$', hosts, name='hosts'),
    url(r'^gethosts/extinfo$', hosts_ext_info, name='hosts_ext_info'),
    url(r'^backup_checks.cfg$', backup_checks, name='backup_checks_old'),
#    url(r'^load_checks.cfg$', generic_checks, {'template':'nagios/load_checks.cfg'}, name='load_checks'),
    url(r'^getchecks/backup$', backup_checks, name='backup_checks'),
    url(r'^getchecks/(?P<name>[a-z]+)$', get_checks, name='get_checks'),
)
