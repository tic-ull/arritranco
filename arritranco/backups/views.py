# Create your views here.

from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.response import Response
from models import FileBackupTask, FileBackupProduct
from scheduler.models import TaskCheck

class BackupFileCheckerView(ResponseMixin, View):
    """An example view using Django 1.3's class based views.
    Uses djangorestframework's RendererMixin to provide support for multiple output formats."""

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        list_of_tasks = {}
        f = {}
        if 'checker' in request.GET:
            f = {'checker_fqdn':request.GET['checker']}
        for fbt in FileBackupTask.objects.filter(active = True, machine__up = True, **f):
            last_run = fbt.last_run()
            try:
                TaskCheck.objects.get(task = fbt, task_time = last_run)
            except TaskCheck.DoesNotExist:
                previous_run = fbt.last_run(last_run)
                if fbt.machine.fqdn not in list_of_tasks:
                    list_of_tasks[fbt.machine.fqdn] = []
                task = {
                        'checker':fbt.checker_fqdn,
                        'directory':fbt.directory,
                        'last_run': last_run,
                        'previous_run':previous_run,
                        'files':[],
                    }
                for product in FileBackupProduct.objects.filter(file_backup_task = fbt):
                    task['files'].append({
                        'pattern':product.file_pattern.pattern,
                        'start_seq':product.start_seq,
                        'end_seq':product.end_seq,
                        'variable_percentage':product.variable_percentage,
                        })
                list_of_tasks[fbt.machine.fqdn].append(task)

        response = Response(200, list_of_tasks)
        return self.render(response)

