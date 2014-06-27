from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns('',
                       url(r'^$', BackupTaskListCreateView.as_view()),
                       url(r'^tsm/hosts/$', TSMHostsView.as_view(), name='tsm-hosts'),
                       url(r'^todo/$', FileBackupsTodo.as_view(), name='backups-todo'),
                       url(r'^backupfilechecker/$', BackupFileCheckerView.as_view(), name='backup-file-checker'),
                       url(r'^filesToCompress$', FilesToCompressView.as_view(), name='backup-files-to-compress'),
                       url(r'^filesToDelete$', FilesToDeleteView.as_view(), name='backup-files-to-delete'),
                       url(r'^addBackupFile$', add_backup_file, name="addBackupFile"),
                       url(r'^backupFileInfo$', GetBackupFileInfo.as_view(), name="BackupFileInfo"),
                       url(r'^addWindowsBackupFile$', add_backup_file, {'windows': True}, name="addWindowsBackupFile"),
                       url(r'^registerFileFromChecker$', register_file_from_checker, name="register_file_from_checker"),
                       url(r'^addCompressedBackupFile$', add_compressed_backup_file, name="addCompressedBackupFile"),
                       url(r'^(?P<pk>\d+)/$', BackupTaskView.as_view()),
)
