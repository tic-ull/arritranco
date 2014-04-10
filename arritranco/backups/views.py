# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView, Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status as httpstatus
from serializers import *
from django.conf import settings
from models import FileBackupTask, FileBackupProduct, BackupFile, TSMBackupTask, BackupTask
from scheduler.models import TaskCheck, TaskStatus
from scheduler.views import Todo
from inventory.models import Machine
import datetime
import math
import os
import logging

logger = logging.getLogger(__name__)

MACHINE_NOT_FOUND_ERROR = 'Machine object not found'


class BackupFileCheckerView(APIView):
    """List all non Ok tasks  """

    def get(self, request, format=None):
        list_of_tasks = {}
        tasks = []
        f = {}
        if 'checker' in request.GET:
            f = {'checker_fqdn': request.GET['checker']}
        for fbt in FileBackupTask.objects.filter(active=True, machine__up=True, **f):
            last_run = fbt.last_run()
            try:
                tc = TaskCheck.objects.get(task=fbt, task_time=last_run)
                status = tc.last_status
                if (isinstance(status, TaskStatus) and status.status == 'Ok') or (status == 'Ok'):
                    continue
            except TaskCheck.DoesNotExist:
                pass

            if fbt.machine.fqdn not in list_of_tasks:
                list_of_tasks[fbt.machine.fqdn] = []
            list_of_tasks[fbt.machine.fqdn].append(FileBackupTaskSerializer(fbt).data)

        return Response(list_of_tasks, status=httpstatus.HTTP_200_OK)


def add_backup_file(request, machine=False, windows=False):
    """Add a file to a backup task."""
    # We have to know from what host we are being called.
    logger.debug('Adding backup file')

    if not machine:
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'], filter_up=True)
        if not machine:
            logger.error('There is no machine for address: %s' % request.META['REMOTE_ADDR'])
            raise Http404(MACHINE_NOT_FOUND_ERROR)

    if not request.GET.has_key('filename'):
        logger.error('No filename in request')
        raise Http404("filename")

    if not request.GET.has_key('filedate'):
        logger.error('No file date in request')
        raise Http404("Filedate")
    #FIXME: check if windows part is necesary.
    if windows and not request.GET.has_key('filetime'):
        logger.error('No file time in request')
        raise Http404("Filetime")

    if not windows and not 'filesize' in request.GET:
        logger.error('No file size in request')
        raise Http404("Filesize")

    filename = request.GET['filename']
    logger.debug('filename: %s', filename)
    if windows:
        logger.debug('Windows file')
        filedate = map(int, request.GET['filedate'].split('/'))
        filetime = map(int, request.GET['filetime'].split(':'))
        filedate = datetime.datetime(filedate[2], filedate[1], filedate[0], filetime[0], filetime[1], filetime[2])
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
        msg = "There is no pattern for this file: %s" % filename
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
    tch, created = TaskCheck.objects.get_or_create(
        task=fbp.file_backup_task,
        task_time=tch_time
    )
    if created:
        logger.debug('TaskCheck created %s' % tch)
    else:
        logger.debug('TaskCheck already exists %s' % tch)
    bf, created = BackupFile.objects.get_or_create(
        file_backup_product=fbp,
        task_check=tch,
        original_file_name=filename,
        original_date=filedate,
        original_file_size=filesize
    )
    if created:
        logger.debug('BackupFile created %s' % bf)
    else:
        logger.debug('BackupFile already exists %s' % bf)
    return HttpResponse("Ok")


def register_file_from_checker(request):
    """Associate a file with his schedule from the copies repo."""
    if not request.GET.has_key('host'):
        logger.warning("Host missing calling register_file_from_checker")
        raise Http404("Host missing")

    machine = Machine.get_by_addr(request.GET['host'])
    if not machine:
        logger.error(MACHINE_NOT_FOUND_ERROR)
        raise Http404(MACHINE_NOT_FOUND_ERROR)

    return add_backup_file(request, machine)


def add_compressed_backup_file(request):
    """Compressed file tied with original backup file."""
    id = directory = compressedmd5 = originalmd5 = None

    if 'checker' in request.GET:
        machine = Machine.get_by_addr(request.GET['checker'])
    else:
        machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
    if not machine:
        logger.error(MACHINE_NOT_FOUND_ERROR)
        raise Http404(MACHINE_NOT_FOUND_ERROR)

    logger.debug('add_compressed_backup_file called from %s', machine.fqdn)

    if not 'filedate' in request.GET:
        raise Http404("Filedate")
    if not 'filesize' in request.GET:
        raise Http404("Filesize")
    if not 'compressedfilename' in request.GET:
        raise Http404("compressedfilename")
    if 'compressedmd5' in request.GET:
        compressedmd5 = request.GET['compressedmd5']
    if 'originalmd5' in request.GET:
        originalmd5 = request.GET['originalmd5']
    if 'id' in request.GET:
        logger.debug('Adding compressed backupfile using id')
        id = request.GET['id']
    if 'directory' in request.GET:
        logger.debug('Adding compressed backupfile using filename and path')
        directory = request.GET['directory']
    if not (id or directory):
        return HttpResponseBadRequest()

    compressed_file_name = request.GET['compressedfilename']
    filedate = datetime.datetime.fromtimestamp(float(request.GET['filedate']))
    filesize = request.GET['filesize']
    if id:
        logger.debug('id: %s', id)
        backup_file = get_object_or_404(BackupFile, pk=id)
    else:
        logger.debug('path: %s', directory)
        logger.debug('filename: %s', os.path.splitext(compressed_file_name)[0])
        backup_file = get_object_or_404(BackupFile,
                                        original_file_name__startswith=os.path.splitext(compressed_file_name)[0],
                                        file_backup_product__file_backup_task__directory__startswith=directory
        )
    backup_file.compressed_file_name = compressed_file_name
    backup_file.compressed_file_size = filesize
    backup_file.compressed_date = filedate
    if compressedmd5:
        backup_file.compressed_md5 = compressedmd5
    if originalmd5:
        backup_file.original_md5 = originalmd5
    backup_file.save()
    return HttpResponse("Ok")


class BackupTaskView(generics.RetrieveAPIView):
    """Detail of BackupTask."""
    queryset = BackupTask.objects.all()
    serializer_class = BackupTaskSerializer


class BackupTaskListCreateView(generics.ListCreateAPIView):
    """List or create BackupTask instances."""
    queryset = BackupTask.objects.all()
    serializer_class = BackupTaskSerializer
    paginate_by = 50
    paginate_by_param = 'page_size'


class FileBackupsTodo(Todo):
    model = FileBackupTask
    serializer = FileBackupTaskSerializer


class FilesToCompressView(APIView):
    """Returns a json with the list of files to be compressed"""

    def get(self, request):
        if 'checker' in request.GET:
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        logger.debug('Files to compress in: %s', machine.fqdn)
        tocompress = []
        totalsize = 0
        for bf in BackupFile.objects.filter(
                compressed_file_name='', deletion_date__isnull=True,
                file_backup_product__file_backup_task__checker_fqdn=machine.fqdn).order_by('-original_date'):
            tocompress.append(BackupFileSerializer(bf).data)
            totalsize += bf.original_file_size
            if (totalsize > settings.MAX_COMPRESS_GB * 1024 ** 3):
                logger.debug('Total size max reached: %s', totalsize)
                break
        logger.debug('Total files: %s', len(tocompress))
        return Response(tocompress, status=httpstatus.HTTP_200_OK)


class FilesToDeleteView(APIView):
    """Returns a json with the list of files to be deleted"""

    def task_checks_older_than_max_days_in_disk(self, task):
        return list(TaskCheck.objects.filter(
            task_time__lte=datetime.datetime.now() - datetime.timedelta(days=task.days_in_hard_drive),
            task=task
        )
        )

    def post(self, request):
        if 'checker' in request.GET:
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        if not 'deleted_files' in request.POST:
            logger.warning('Lack of  deleted_files POST data')
            return HttpResponseBadRequest()
        files_to_delete = request.POST.getlist('deleted_files')
        logger.debug('deleted_files: %s', files_to_delete)
        response = []
        for f in files_to_delete:
            directory, filename = os.path.split(f)
            logger.debug('Deleting directory: %s file: %s', directory, filename)
            status = False
            for backupFile in BackupFile.objects.filter(
                    (Q(original_file_name=filename) | Q(compressed_file_name=filename)),
                    Q(file_backup_product__file_backup_task__directory__startswith=directory),
                    Q(file_backup_product__file_backup_task__checker_fqdn=machine.fqdn)):
                backupFile.deletion_date = datetime.datetime.now()  # Se mantiene la entrada en la bd hasta que desaparezca de las cintas
                backupFile.save()
                status = True
            response.append((f, status))
            if status:
                logger.debug('Deleted')
            else:
                logger.debug('Already deleted, nothing to do')
        response = Response(response, httpstatus.HTTP_200_OK)
        return (response)

    def get(self, request):
        if 'checker' in request.GET:
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        filter = {'taskcheck__backupfile__deletion_date__isnull': True,  # isnull matches checks without backups
                  'taskcheck__backupfile__isnull': False}  # so we check that there are 1+ backupfiles
        if 'host' in request.GET:
            host = Machine.get_by_addr(request.GET['host'])
            filter['machine'] = host

        logger.debug('Files to delete in: %s', machine.fqdn)
        today = datetime.date.today()
        task_to_delete = []
        for task in FileBackupTask.objects.filter(checker_fqdn=machine.fqdn, **filter).distinct():
            logger.debug('Delete files for task: %s: %s', task, task.description)
            task_to_delete += self.task_checks_older_than_max_days_in_disk(task)
            first_month_day = datetime.datetime(today.year, today.month, 1, 0, 0, 0)
            #            first_month_day = datetime.datetime(last_month_day.year, last_month_day.month, 1, 0, 0, 0)

            for m in range(1, 12):
                last_month_day = first_month_day
                tmp_day = last_month_day - datetime.timedelta(minutes=1)
                first_month_day = datetime.datetime(tmp_day.year, tmp_day.month, 1, 0, 0, 0)
                logger.debug('first month day: %s, Last month day: %s', first_month_day, last_month_day)
                tchs = []

                for tch in TaskCheck.objects.filter(
                        task=task,
                        task_time__gte=first_month_day,
                        task_time__lte=last_month_day,
                        backupfile__deletion_date__isnull=True,
                        backupfile__original_date__isnull=False).select_related('task').distinct().order_by(
                        'task_time'):
                    if tch.backupfile_set.filter(deletion_date__isnull=True).count():
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
            for bf in tch.backupfile_set.filter(deletion_date__isnull=True):
                files_to_delete.append(BackupFileToDeleteSerializer(bf).data)
                logger.debug('Adding: %s', bf.path)
        logger.debug("End filling files_to_delete")
        return Response(files_to_delete, httpstatus.HTTP_200_OK)


class GetBackupFileInfo(APIView):
    """Returns json with info about a file matching with filename."""

    def get(self, request):
        if not 'file_name' in request.GET:
            logger.debug('No file name in request')
            return HttpResponseBadRequest()
        if not 'directory' in request.GET:
            logger.debug('No directory in request')
            return HttpResponseBadRequest()
        if 'checker' in request.GET:
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
            Q(file_backup_product__file_backup_task__checker_fqdn=machine.fqdn) &
            Q(file_backup_product__file_backup_task__directory=request.GET['directory']) &
            (
                Q(compressed_file_name=file_name) |
                Q(original_file_name=file_name) |
                Q(compressed_file_name=os.path.splitext(file_name)[0]) |
                Q(original_file_name=os.path.splitext(file_name)[0])
            )
        ).order_by('original_date')
        if file_info.count() == 0:
            logger.debug('File not found in DB')
            raise Http404('There is no such file in database')
        info = BackupFileInfoSerializer(file_info[0]).data
        return Response(info, httpstatus.HTTP_200_OK)


class TSMHostsView(APIView):
    """Lists of hosts baked up with tsm"""

    def get(self, request):
        if 'checker' in request.GET:
            machine = Machine.get_by_addr(request.GET['checker'])
        else:
            machine = Machine.get_by_addr(request.META['REMOTE_ADDR'])
        if not machine:
            logger.error(MACHINE_NOT_FOUND_ERROR)
            raise Http404(MACHINE_NOT_FOUND_ERROR)

        if 'tsm_server' in request.GET:
            qs = TSMBackupTask.objects.filter(tsm_server=request.GET['tsm_server'])
        else:
            qs = TSMBackupTask.objects.all()
        logger.debug('TSM Hosts')
        totalsize = 0
        tsm_hosts = []
        for bt in qs:
            tsm_hosts.append(HostTSMBackupTaskSerializer(bt).data)
            # tsm_hosts.append({
            #     'fqdn':bt.machine.fqdn,
            #     'tsm_server':bt.tsm_server,
            #     'ipaddress':bt.machine.get_service_ip(),
            #     })
        logger.debug('Total hosts: %s', len(tsm_hosts))
        return Response(tsm_hosts, httpstatus.HTTP_200_OK)
