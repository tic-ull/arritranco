from django.core.management.base import BaseCommand, CommandError
from backups.models import BackupFile, FileBackupTask, BackupTask
from scheduler.models import TaskCheck, TaskStatus
import datetime
import settings
import sys


class Command(BaseCommand):
    args = ''
    help = 'Clean the TaskChecks and BackupFile'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Deleting backupFiles')

            BackupFile.objects.exclude(deletion_date__isnull=True).filter(
                deletion_date__lt=(datetime.datetime.now() -
                                   datetime.timedelta(days=settings.BACKUP_FILE_TIME_TO_DELETE))).delete()

            self.stdout.write('Deleting TaskChecks')

            for taskcheck in TaskCheck.objects.all():
                try:
                    FileBackupTask.objects.get(id=taskcheck.task.id)
                    if not BackupFile.objects.filter(task_check=taskcheck):
                        TaskStatus.objects.filter(task_check=taskcheck).delete()
                        taskcheck.delete()
                except FileBackupTask.DoesNotExist:
                    pass

        except Exception as e:
            self.stdout.write('Fail : ' + e.message)
            return -1
        except:
            fail = "Unknow exeption !\n sys exc info : \n"
            for fails in sys.exc_info()[0:5]:
                fail += str(fails) + "\n"
            self.stdout.write('Fail : ' + fail)
            return -2

        self.stdout.write('Successfully cleaned TaskChecks and BackupFile')
