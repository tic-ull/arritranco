from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

from backups.admin_views import BackupGrid
from backups.admin_views import BackupGridList

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/backups/grid/', BackupGrid.as_view(), name='backup-grid'),
    url(r'^admin/backups/grid-list/', BackupGridList.as_view(), name='backup-grid-list'),
    url(r'^admin/hardware/', include('hardware.admin_urls')),
    url(r'^admin/inventory/', include('inventory.admin_urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^inventory/', include('inventory.urls')),    
    (r'^rest/backup/', include('backups.urls')),
    (r'^api/v1/rest/backup/', include('backups.urls')),
    (r'^bcfg2/backup/', include('backups.bcfg2_urls')),
    (r'^bcfg2/inventory/', include('inventory.bcfg2_urls')),
    (r'^rest/scheduler/', include('scheduler.urls')),
    (r'^api/v1/rest/scheduler/', include('scheduler.urls')),
    (r'^monitoring/nagios/', include('monitoring.nagios.urls')),
    (r'^api/v1/monitoring/nagios/', include('monitoring.nagios.urls')),
    (r'^monitoring/sondas/', include('monitoring.sondas.urls')),
    (r'^api/v1/monitoring/sondas/', include('monitoring.sondas.urls')),
    (r'^maps/', include('inventory.maps_urls')),
    (r'^', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                                                'show_indexes': True}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,
                                                                 'show_indexes': True}),
    )
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

