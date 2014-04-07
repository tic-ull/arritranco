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

            for filebackuptask in FileBackupTask.objects.filter(taskcheck__backupfile__isnull=True).distinct():
                for taskcheck in filebackuptask.taskcheck_set.filter(backupfile__isnull=True).distinct():
                    taskcheck.taskstatus_set.all().delete()
                    taskcheck.delete()

            f = open("fbt_no_taskcheck.csv", "w")
            for filebackuptask in FileBackupTask.objects.filter(taskcheck__isnull=True, active=True, machine__up=True):
                f.write(str(filebackuptask.id) + "," + str(filebackuptask.machine.fqdn) + "\n")
            f.close()

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
