# Create your views here.
from djangorestframework.views import View
from models import Task
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
