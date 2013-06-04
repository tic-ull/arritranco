from django.conf.urls.defaults import patterns, url
try:
    from djangorestframework.resources import ModelResource
    from djangorestframework.views import ListOrCreateModelView, InstanceModelView
except:
    pass

from models import Task, TaskCheck
from views import Todo, TaskCheckListCreateView, TaskStatusView, TaskDetailView, TaskListCreateView, TaskCheckDetailView

urlpatterns = patterns('',
    url(r'^taskchecks/$', TaskCheckListCreateView.as_view(), name='taskchecks'),
    url(r'^taskchecks/(?P<pk>[0-9]+)$', TaskCheckDetailView.as_view(), name='taskcheckdetail'),
    url(r'^tasks$', TaskListCreateView.as_view(), name='tasks'),
    url(r'^tasks/(?P<pk>[0-9]+)$', TaskDetailView.as_view(), name='tasksdetail'),
    url(r'^tasks/(?P<pk>[0-9]+)/status$', TaskStatusView.as_view(), name='taskstatus'),
    url(r'^todo/$', Todo.as_view(), name='tasks-todo'), 
    url(r'^(?P<pk>[^/]+)/$', TaskCheckDetailView.as_view()),
)
