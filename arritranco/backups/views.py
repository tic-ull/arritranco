# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse 
from django.shortcuts import get_object_or_404
from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.response import Response
from models import FileBackupTask, FileBackupProduct, BackupFile
from scheduler.models import TaskCheck
from inventory.models import Machine
import datetime
import math
import os

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
                tc = TaskCheck.objects.get(task = fbt, task_time = last_run)
                status = tc.get_status():
                if (isinstance(status, TaskStatus) and status.status == 'Ok') or (status == 'Ok'):
                    continue
            except TaskCheck.DoesNotExist:
                pass
            previous_run = fbt.last_run(last_run)
            if fbt.machine.fqdn not in list_of_tasks:
                list_of_tasks[fbt.machine.fqdn] = []
            task = {
                    'id':fbt.id,
                    'description':fbt.description,
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

def add_backup_file (request, machine = False, windows = False):
    """
        Asocia un fichero a una planificación de una máquina.
    """
    # Hay que saber desde qué máquina nos están consultando.
    if not machine:
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            raise Http404('There is no machine for address: %s' % request.META['REMOTE_ADDR'])
    if not request.GET.has_key('filename'):
        raise Http404("filename")
    if not request.GET.has_key ('filedate'):
        raise Http404("Filedate")
    if windows and not request.GET.has_key ('filetime'):
        raise Http404("Filetime")
    if not windows and not request.GET.has_key('filesize'):
        raise Http404("Filesize")
    filename = request.GET['filename']
    if windows:
        filedate = map(int, request.GET['filedate'].split ('/'))
        filetime = map (int, request.GET['filetime'].split (':'))
#        filedate = datetime.datetime.now ()
        filedate = datetime.datetime.now (filedate[2], filedate[1], filedate[0], filetime[0], filetime[1], filetime[2])
        filesize = 0
    else:
        filedate = datetime.datetime.fromtimestamp(float(request.GET['filedate']))
        filesize = request.GET['filesize']
    fbp = FileBackupTask.get_fbp(machine, filename)
    if not fbp:
        return HttpResponse ("There is no pattern for this file")
    next_run = fbp.file_backup_task.next_run(filedate)
    previous_run = fbp.file_backup_task.last_run(filedate)
    if (abs(next_run - filedate) >= abs(filedate - previous_run)):
        tch_time = next_run
    else:
        tch_time = previous_run
    tch, created = TaskCheck.objects.get_or_create (
            task = fbp.file_backup_task,
            task_time = tch_time
        )
    bf, created = BackupFile.objects.get_or_create (
            file_backup_product = fbp,
            task_check = tch,
            original_file_name = filename,
            original_date = filedate,
            original_file_size = filesize
        )
    return HttpResponse("Ok")

def register_file_from_checker(request):
    """
        Asocia un fichero con su planificación partiendo del repositorio de copias.
    """
    if not request.GET.has_key ('host'):
        raise Http404("Host")
    machine = Machine.get_by_addr(request.GET['host'])
    if not machine:
        raise Http404('Machine object not found')
    return add_backup_file(request, machine)

def add_compressed_backup_file (request):
    """
        Asocia un fichero comprimido a una su fichero de backup.
    """
    compressedmd5 = originalmd5 = None
    if not request.GET.has_key('id'):
        raise Http404("id")
    if not request.GET.has_key ('filedate'):
        raise Http404("Filedate")
    if not request.GET.has_key('filesize'):
        raise Http404("Filesize")
    if not request.GET.has_key('compressedfilename'):
        raise Http404("compressedfilename")
    if request.GET.has_key('compressedmd5'):
        compressedmd5 = request.GET['compressedmd5']
    if request.GET.has_key('originalmd5'):
        originalmd5 = request.GET['originalmd5']
    id = request.GET['id']
    compressed_file_name = request.GET['compressedfilename']
    filedate = datetime.datetime.fromtimestamp(float(request.GET['filedate']))
    filesize = request.GET['filesize']
    backup_file = get_object_or_404 (BackupFile, pk = id)
    backup_file.compressed_file_name = compressed_file_name
    backup_file.compressed_file_size = filesize
    backup_file.compressed_date = filedate
    if compressedmd5:
        backup_file.compressed_md5 = compressedmd5
    if originalmd5:
        backup_file.original_md5 = originalmd5
    backup_file.save ()
    return HttpResponse("Ok")

class FilesToCompressView(ResponseMixin, View):
    """An example view using Django 1.3's class based views.
    Uses djangorestframework's RendererMixin to provide support for multiple output formats."""

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            raise Http404('Machine object not found')
        tocompress = []
        for bf in BackupFile.objects.filter (compressed_file_name = '',
                file_backup_product__file_backup_task__checker_fqdn = machine.fqdn):
            tocompress.append (
                [
                    bf.id,
                    os.path.join(bf.file_backup_product.file_backup_task.directory, bf.original_file_name)
                ])
        response = Response(200, tocompress)
        return self.render(response)

class FilesToDeleteView(ResponseMixin, View):
    """An example view using Django 1.3's class based views.
    Uses djangorestframework's RendererMixin to provide support for multiple output formats."""

    renderers = DEFAULT_RENDERERS

    def task_checks_older_than_max_days_in_disk(self, task):
        return list(TaskCheck.objects.filter(task_time__lte = task.days_in_hard_drive))

    def get(self, request):
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            raise Http404('Machine object not found')
        task_to_delete = []
        today = datetime.date.today()
        last_month_day = datetime.datetime(today.year, today.month, 1, 0, 0, 0) - datetime.timedelta(minutes = 1)
        first_month_day = datetime.datetime(last_month_day.year, last_month_day.month, 1, 0, 0, 0)
        for task in FileBackupTask.objects.filter(checker = machine.fqdn):
            task_to_delete += self.task_checks_older_than_max_days_in_disk(task)
            tchs = TaskCheck.objects.filter(
                task = task,
                task_time__gte = first_month_day,
                task_time__lte = last_month_day).orderby('task_time')
            if len(tchs) > task.max_backup_month:
                step = float(len(tchs)) / (len(tchs) - task.max_backup_month)
                last = len(tchs) - 1 - step
                while last > 0:
                    task_to_delete.append(tchs[int(math.ceil(last))])
                    last -= step
        files_to_delete = []
        for tch in task_to_delete:
            directory = tch.task.backuptask.filebackuptask.directory
            for bf in tch.backupfile_set.all():
                path = os.path.join(directory, bf.compressed_file_name or bf.original_file_name)
                files_to_delete.append({'path':path, 'pk':bf.id})

        response = Response(200, files_to_delete)
        return self.render(response)
