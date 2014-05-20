# Create your views here.

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status as httpstatus
from rest_framework.views import Response

from models import Task, TaskCheck
from django.shortcuts import get_object_or_404
from serializers import TaskCheckSerializer, TaskSerializer, TaskStatusSerializer
import datetime


class Todo(ListAPIView):
    """Class to handle tasks todo."""
    model = Task
    serializer = TaskSerializer

    def get(self, request, *args, **kwargs):
        """Return a list of all the tasks to be done."""
        start_time = None
        end_time = None
        if request.GET.has_key('start_time'):
            start_time = datetime.datetime.fromtimestamp(float(request.GET['start_time']))
        if request.GET.has_key('end_time'):
            end_time = datetime.datetime.fromtimestamp(float(request.GET['end_time']))
        queryset = self.model.objects.todo(start_time, end_time)

        return Response(self.serializer(queryset).data, httpstatus.HTTP_200_OK)


class TaskListCreateView(ListCreateAPIView):
    """List and create view for task items, paginated 50 items."""

    model = Task
    serializer = TaskSerializer
    paginate_by = 50
    paginate_by_param = 'page_size'

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """Get or update or delete view for task items."""

    model = Task
    serializer = TaskSerializer

class TaskCheckListCreateView(ListCreateAPIView):
    """List or create TaskChecks for a task"""

    model = TaskCheck
    serializer = TaskCheckSerializer
    paginate_by = 50
    paginate_by_param = 'page_size'

class TaskCheckDetailView(RetrieveUpdateDestroyAPIView):
    """Get or update or delete a instance of TaskCheck."""

    model = TaskCheck
    serializer = TaskCheckSerializer

class TaskStatusView(APIView):
    """Shows and updates task status."""

    serializer = TaskStatusSerializer

    def get(self, request, pk = None):
        """Handle GET requests.Returns a simple string indicating last status for a task."""

        d = None
        if 'time' in request.GET:
            try:
                d = datetime.datetime.strptime(request.GET['time'], '%Y-%m-%d %H:%M:%S')
            except ValueError, e:
                return e
        if pk is not None:
            task = get_object_or_404(Task, pk=pk)
            return Response(self.serializer(task.get_status(d)).data, httpstatus.HTTP_200_OK)
        else:
            return "No task"

    def post(self, request, pk = None):
        """Handle POST requests, with  validation. Returns the new status if updated succeeded."""

        task = get_object_or_404(Task, pk=pk)

        data = self.serializer(data = request.DATA)
        if data.is_valid():
            cleaned_data = data.data
        else:
            return Response(self.serializer.errors, httpstatus.HTTP_400_BAD_REQUEST)
        task_time = task.last_run()
        task.update_status(task_time, cleaned_data['status'], cleaned_data['comment'])
        return Response(self.serializer(task.get_status()).data, httpstatus.HTTP_200_OK)
