# Create your views here.
from djangorestframework.views import View
from djangorestframework.response import Response
from djangorestframework import status
from models import Task
from forms import TaskCheckForm
from django.shortcuts import get_object_or_404

import datetime

class Todo(View):
    '''
        Class to handle tasks todo
    '''
    queryset = Task.objects.all()

    def get(self, request):
        '''
            Return a list of all the tasks to be done
        '''
        if request.GET.has_key('start_time'):
            start_time = datetime.datetime.fromtimestamp(float(request.GET['start_time']))
        if request.GET.has_key('end_time'):
            end_time = datetime.datetime.fromtimestamp(float(request.GET['end_time']))
        return Task.todo(queryset = self.queryset)

class TaskStatusView(View):
    """
    Shows and updates task status.
    """
    form = TaskCheckForm

    def get(self, request, task = None):
        """
        Handle GET requests.
        Returns a simple string indicating last status for a task
        """
        d = None
        if 'time' in request.GET:
            try:
                d = datetime.datetime.strptime(request.GET['time'], '%Y-%m-%d %H:%M:%S')
            except ValueError, e:
                return e
        if task is not None:
            task = get_object_or_404(Task, pk=task)
            return task.get_status(d)
        else:
            return "No task"

    def post(self, request, task = None):
        """
        Handle POST requests, with form validation.
        Returns a simple string indicating what content was supplied.
        """
        form = self.get_bound_form(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
        else:
            return "Error: %s" % (request.POST)
        task = cleaned_data['task']
        task.update_status(cleaned_data['task_time'], cleaned_data['status'], cleaned_data['comment'])
        return "Task status updated status: %s" % (cleaned_data['status'])
