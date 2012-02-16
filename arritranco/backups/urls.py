from django.conf.urls.defaults import patterns, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from models import BackupTask, TSMBackupTask, R1BackupTask
from scheduler.models import Task
from scheduler.views import Todo
from views import BackupFileCheckerView

class BackupTaskResource(ModelResource):
    model = BackupTask

class BackupsTodo(Todo):
    queryset = BackupTask.objects.all()

class TSMBackupsTodo(BackupsTodo):
    queryset = TSMBackupTask.objects.all()

class R1BackupsTodo(BackupsTodo):
    queryset = R1BackupTask.objects.all()


urlpatterns = patterns('',
    url(r'^$', ListOrCreateModelView.as_view(resource=BackupTaskResource)),
    url(r'^tsm/todo/$', TSMBackupsTodo.as_view(), name='tsm-backups-todo'), 
    url(r'^r1/todo/$', R1BackupsTodo.as_view(), name='r1-backups-todo'), 
    url(r'^todo/$', BackupsTodo.as_view(), name='backups-todo'), 
    url(r'^backupfilechecker/$', BackupFileCheckerView.as_view(), name='backup-file-checker'),
    url(r'^(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=BackupTaskResource)),
)
