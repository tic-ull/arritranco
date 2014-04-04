from django.core.management.base import BaseCommand, CommandError
from backups.models import BackupFile
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
            for backupFile in BackupFile.objects.all():
                if backupFile.deletion_date is None:
                    backupFile.delete()
                elif backupFile.deletion_date < (datetime.datetime.now() +
                                               datetime.timedelta(days=settings.BACKUP_FILE_TIME_TO_DELETE)):
                    backupFile.delete()

            self.stdout.write('Deleting TaskChecks')
            for taskcheck in TaskCheck.objects.all():
                if BackupFile.objects.filter(task_check=taskcheck) is None:
                    for taskstatu in TaskStatus.objects.filter(taskcheck=taskcheck):
                        taskstatu.delete()
                    taskcheck.delete()
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
