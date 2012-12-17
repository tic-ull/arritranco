# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.response import Response
from django.conf import settings
from models import FileBackupTask, FileBackupProduct, BackupFile, TSMBackupTask
from scheduler.models import TaskCheck, TaskStatus
from inventory.models import Machine
import datetime
import math
import os
import logging
logger = logging.getLogger(__name__)

MACHINE_NOT_FOUND_ERROR = 'Machine object not found'

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
                status = tc.get_status()
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

def add_backup_file(request, machine = False, windows = False):
    """
        Asocia un fichero a una planificación de una máquina.
    """
    # Hay que saber desde qué máquina nos están consultando.
    logger.debug('Adding backup file')

    if not machine:
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error('There is no machine for address: %s' % request.META['REMOTE_ADDR'])
            raise Http404(MACHINE_NOT_FOUND_ERROR)

    if not request.GET.has_key('filename'):
        logger.error('No filename in request')
        raise Http404("filename")

    if not request.GET.has_key ('filedate'):
        logger.error('No file date in request')
        raise Http404("Filedate")

    if windows and not request.GET.has_key ('filetime'):
        logger.error('No file time in request')
        raise Http404("Filetime")

    if not windows and not request.GET.has_key('filesize'):
        logger.error('No file size in request')
        raise Http404("Filesize")

    filename = request.GET['filename']
    logger.debug('filename: %s', filename)
    if windows:
        logger.debug('Windows file')
        filedate = map(int, request.GET['filedate'].split ('/'))
        filetime = map (int, request.GET['filetime'].split (':'))
        filedate = datetime.datetime.now (filedate[2], filedate[1], filedate[0], filetime[0], filetime[1], filetime[2])
        filesize = 0
    else:
        logger.debug('Unix file')
        try:
            filedate = datetime.datetime.fromtimestamp(float(request.GET['filedate']))
            # Croniter doest not get seconds difference, to ensure last_run is this run we increment 1 min to filetime
            filedate = filedate + datetime.timedelta(minutes=1)

        except ValueError, e:
            logger.error(e)
            return HttpResponse(e)
        filesize = request.GET['filesize']
    fbp = FileBackupTask.get_fbp(machine, filename)
    if not fbp:
        msg = "There is no pattern for this file"
        logger.error(msg)
        return HttpResponse(msg)
    next_run = fbp.file_backup_task.next_run(filedate)
    previous_run = fbp.file_backup_task.last_run(filedate)
    if (abs(next_run - filedate) <= abs(filedate - previous_run)):
        tch_time = next_run
    else:
        tch_time = previous_run
    if tch_time > datetime.datetime.now():
        logger.error('Future backup')
    tch, created = TaskCheck.objects.get_or_create (
            task = fbp.file_backup_task,
            task_time = tch_time
        )
    if created:
        logger.debug('TaskCheck created')
    else:
        logger.debug('TaskCheck already exists')
    bf, created = BackupFile.objects.get_or_create (
            file_backup_product = fbp,
            task_check = tch,
            original_file_name = filename,
            original_date = filedate,
            original_file_size = filesize
        )
    if created:
        logger.debug('BackupFile created')
    else:
        logger.debug('BackupFile already exists')
    return HttpResponse("Ok")

def register_file_from_checker(request):
    """
        Asocia un fichero con su planificación partiendo del repositorio de copias.
    """
    if not request.GET.has_key('host'):
        logger.warning("Host missing calling register_file_from_checker")
        raise Http404("Host missing")

    machine = Machine.get_by_addr(request.GET['host'])
    if not machine:
        logger.error(MACHINE_NOT_FOUND_ERROR)
        raise Http404(MACHINE_NOT_FOUND_ERROR)

    return add_backup_file(request, machine)

def add_compressed_backup_file (request):
    """
        Asocia un fichero comprimido a una su fichero de backup.
    """
    id = directory = compressedmd5 = originalmd5 = None

    if request.GET.has_key('checker'):
        machine = Machine.get_by_addr(request.GET['checker'])
    else:
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
    if not machine:
        logger.error(MACHINE_NOT_FOUND_ERROR)
        raise Http404(MACHINE_NOT_FOUND_ERROR)

    logger.debug('add_compressed_backup_file called from %s', machine.fqdn)

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
    if request.GET.has_key('id'):
        logger.debug('Adding compressed backupfile using id')
        id = request.GET['id']
    if request.GET.has_key('directory'):
        logger.debug('Adding compressed backupfile using filename and path')
        directory = request.GET['directory']
    if not (id or directory):
        return HttpResponseBadRequest()

    compressed_file_name = request.GET['compressedfilename']
    filedate = datetime.datetime.fromtimestamp(float(request.GET['filedate']))
    filesize = request.GET['filesize']
    if id:
        logger.debug('id: %s', id)
        backup_file = get_object_or_404 (BackupFile, pk = id)
    else:
        logger.debug('path: %s', directory)
        logger.debug('filename: %s', os.path.splitext(compressed_file_name)[0])
        backup_file = get_object_or_404 (BackupFile,
            original_file_name__startswith = os.path.splitext(compressed_file_name)[0],
            file_backup_product__file_backup_task__directory__startswith = directory
            )
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
    """Returns a json with the list of files to be compressed"""

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        logger.debug('Files to compress in: %s', machine.fqdn)
        tocompress = []
        totalsize = 0
        for bf in BackupFile.objects.filter(
                compressed_file_name = '', deletion_date__isnull = True,
                file_backup_product__file_backup_task__checker_fqdn = machine.fqdn).order_by('-original_date'):
            tocompress.append (
                [
                    bf.id,
                    os.path.join(bf.file_backup_product.file_backup_task.directory, bf.original_file_name)
                ])
            totalsize += bf.original_file_size
            if (totalsize > settings.MAX_COMPRESS_GB * 1024**3):
                logger.debug('Total size max reached: %s', totalsize)
                break
        logger.debug('Total files: %s', len(tocompress))
        response = Response(200, tocompress)
        return self.render(response)


class FilesToDeleteView(ResponseMixin, View):
    """An example view using Django 1.3's class based views.
    Uses djangorestframework's RendererMixin to provide support for multiple output formats."""

    renderers = DEFAULT_RENDERERS

    def task_checks_older_than_max_days_in_disk(self, task):
        return list(TaskCheck.objects.filter(
                    task_time__lte = datetime.datetime.now() - datetime.timedelta(days = task.days_in_hard_drive),
                    task = task
                    )
                 )

    def post(self, request):
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        if not request.POST.has_key('deleted_files'):
            return HttpResponseBadRequest()
        files_to_delete = request.POST.getlist('deleted_files')
        logger.debug('deleted_files: %s', files_to_delete)
        response = []
        for f in files_to_delete:
            directory, filename = os.path.split(f)
            logger.debug('Deleting directory: %s file: %s', directory, filename)
            status = False
            for backupFile in BackupFile.objects.filter((Q(original_file_name = filename) | Q(compressed_file_name = filename)),
                                                        Q(file_backup_product__file_backup_task__directory__startswith = directory),
                                                        Q(file_backup_product__file_backup_task__checker_fqdn = machine.fqdn)):
                backupFile.deletion_date = datetime.datetime.now()    # Se mantiene la entrada en la bd hasta que desaparezca de las cintas
                backupFile.save()
                status = True
            response.append((f,status))
            if status:
                logger.debug('Deleted')
            else:
                logger.debug('Already deleted, nothing to do')
        response = Response(200, response)
        return self.render(response)

    def get(self, request):
        if request.GET.has_key('checker'):
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        filter = {}
        if request.GET.has_key('host'):
            host = Machine.get_by_addr(request.GET['host'])
            filter['machine'] = host

        task_to_delete = []
        logger.debug('Files to delete in: %s', machine.fqdn)
        today = datetime.date.today()
        task_to_delete = []
        for task in FileBackupTask.objects.filter(checker_fqdn = machine.fqdn, **filter):
            logger.debug('Delete files for task: %s: %s', task, task.description)
            task_to_delete += self.task_checks_older_than_max_days_in_disk(task)
            first_month_day = datetime.datetime(today.year, today.month, 1, 0, 0, 0)
#            first_month_day = datetime.datetime(last_month_day.year, last_month_day.month, 1, 0, 0, 0)
            for m in range(1, 12):
                last_month_day = first_month_day
                tmp_day = last_month_day -  datetime.timedelta(minutes = 1)
                first_month_day = datetime.datetime(tmp_day.year, tmp_day.month, 1, 0, 0, 0)
                logger.debug('first month day: %s, Last month day: %s', first_month_day, last_month_day)
                tchs = []
                for tch in TaskCheck.objects.filter(
                        task = task,
                        task_time__gte = first_month_day,
                        task_time__lte = last_month_day).order_by('task_time'):
#                    backupfile__deletion_date__isnull = True).order_by('task_time'):
                    if tch.backupfile_set.filter(deletion_date__isnull = True).count():
                        tchs.append(tch)
                logger.debug('len tash checks: %s, max_backup_month: %s', len(tchs), task.max_backup_month)
                if len(tchs) > task.max_backup_month:
                    logger.debug('Selecting task check to delete')
                    step = float(len(tchs)) / (len(tchs) - task.max_backup_month)
                    #last = len(tchs) - 1 - step
                    last = len(tchs) - step
                    logger.debug("Last: %s", last)
                    while last >= 0:
                        task_to_delete.append(tchs[int(math.ceil(last))])
                        logger.debug('Selected: %s', tchs[int(math.ceil(last))].task_time)
                        last -= step
#                else:
#                    break
        files_to_delete = []
        logger.debug("Start filling files_to_delete")
        for tch in task_to_delete:
            directory = tch.task.backuptask.filebackuptask.directory
            logger.debug('Deleting files of task: [%d] %s %s', tch.id, tch, tch.task_time)
            for bf in tch.backupfile_set.filter(deletion_date__isnull = True):
                path = os.path.join(directory, bf.compressed_file_name or bf.original_file_name)
                files_to_delete.append({'path':path, 'pk':bf.id})
                logger.debug('Adding: %s', path)
        logger.debug("End filling files_to_delete")

        response = Response(200, files_to_delete)
        return self.render(response)
 

class GetBackupFileInfo(ResponseMixin, View):
    renderers = DEFAULT_RENDERERS

    def get(self, request):
        if not request.GET.has_key('file_name'):
            logger.debug('No file name in request')
            return HttpResponseBadRequest()
        if not request.GET.has_key('directory'):
            logger.debug('No directory in request')
            return HttpResponseBadRequest()
        if request.GET.has_key('checker'):
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        file_name = request.GET['file_name']
        logger.debug('Searching for: "%s" in "%s"', file_name, request.GET['directory'])
        logger.debug('Checker: "%s"', machine.fqdn)
        file_info = BackupFile.objects.filter(
                Q(file_backup_product__file_backup_task__checker_fqdn = machine.fqdn) &
                Q(file_backup_product__file_backup_task__directory = request.GET['directory']) &
                (
                    Q(compressed_file_name = file_name) |
                    Q(original_file_name = file_name) |
                    Q(compressed_file_name = os.path.splitext(file_name)[0]) |
                    Q(original_file_name = os.path.splitext(file_name)[0])
                )
            ).order_by('original_date')
        if file_info.count() == 0:
            logger.debug('File not found in DB')
            raise Http404('There is no such file in database')
        info = {
            'original_file_name': file_info[0].original_file_name,
            'original_date': file_info[0].original_date,
            'original_file_size': file_info[0].original_file_size,
            'original_md5': file_info[0].original_md5,
            'compressed_file_name': file_info[0].compressed_file_name,
            'compressed_date': file_info[0].compressed_date,
            'compressed_file_size': file_info[0].compressed_file_size,
            'compressed_md5': file_info[0].compressed_md5,
            'id': file_info[0].id,
        }
        response = Response(200, info)
        return self.render(response)


class TSMHostsView(ResponseMixin, View):
    """Lists of hosts baked up with tsm"""

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        if request.GET.has_key('checker'):
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        if request.GET.has_key('tsm_server'):
            qs = TSMBackupTask.objects.filter(tsm_server = request.GET['tsm_server'])
        else:
            qs = TSMBackupTask.objects.all()
        logger.debug('TSM Hosts')
        totalsize = 0
        tsm_hosts = []
        for bt in qs:
            tsm_hosts.append({
                'fqdn':bt.machine.fqdn,
                'tsm_server':bt.tsm_server,
                'ipaddress':bt.machine.get_service_ip(),
                })
        logger.debug('Total hosts: %s', len(tsm_hosts))
        response = Response(200, tsm_hosts)
        return self.render(response)

