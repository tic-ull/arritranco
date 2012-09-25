from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin

from backups.admin_views import BackupGrid

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # FIXME: This url shoud be in backup app
    url(r'^admin/backups/grid/', BackupGrid.as_view(), name='backup-grid'),
    url(r'^admin/hardware/', include('hardware.admin_urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # Necessary for Django Task Scheduler
    #(r'^scheduler/', include('scheduler.urls')),    
    (r'^rest/backup/', include('backups.urls')),    
    (r'^bcfg2/backup/', include('backups.bcfg2_urls')),    
    (r'^bcfg2/inventory/', include('inventory.bcfg2_urls')),    
    (r'^rest/scheduler/', include('scheduler.urls')),    
    (r'^monitoring/nagios/', include('monitoring.nagios.urls')),    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

