from django.template import Library
from django.conf import settings
from backups.models import BackupFile, FileBackupTask
import datetime

register = Library()

@register.inclusion_tag('admin/backups/_files_to_compress.html')
def compress_todo():
    info = {}
    for checker, c in settings.FILE_BACKUP_CHECKERS:
        info[checker] = {
            'files' : BackupFile.objects.filter(
                        compressed_file_name = '',
                        deletion_date__isnull = True,
                        file_backup_product__file_backup_task__checker_fqdn = checker
                      ).order_by('-original_date'),
            'fqdn': checker,
            }
    return {'compress_todo':info}

@register.inclusion_tag('admin/backups/_today_backups.html')
def today_backups():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    list_of_tasks = {}
    number_of_tasks = 0
    for fbt in FileBackupTask.objects.filter(active = True, machine__up = True):
        last_run = fbt.next_run(yesterday)
        while (last_run <= today):
            if fbt.machine.fqdn not in list_of_tasks:
                list_of_tasks[fbt.machine.fqdn] = []
            number_of_tasks += 1
            list_of_tasks[fbt.machine.fqdn].append({
                'time':last_run,
                'task':fbt,
            })
            last_run = fbt.next_run(last_run + datetime.timedelta(minutes = 1))
    return {
            'list_of_tasks':list_of_tasks,
            'number_of_tasks': number_of_tasks,
        }
