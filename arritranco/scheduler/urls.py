from django.conf.urls.defaults import patterns, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from models import Task, TaskCheck
from views import Todo, TaskStatusView

class TaskResource(ModelResource):
    model = Task

class TaskCheckResource(ModelResource):
    model = TaskCheck

urlpatterns = patterns('',
    url(r'^$', ListOrCreateModelView.as_view(resource=TaskResource)),
    url(r'^taskchecks/$', ListOrCreateModelView.as_view(resource=TaskCheckResource)),
    url(r'^taskstatus/$', TaskStatusView.as_view(), {'task':None}, name='taskstatus'),
    url(r'^taskstatus/(?P<task>[^/]+)/$', TaskStatusView.as_view(), name='taskstatus'),
    url(r'^todo/$', Todo.as_view(), name='tasks-todo'), 
    url(r'^(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=TaskCheckResource)),
)
