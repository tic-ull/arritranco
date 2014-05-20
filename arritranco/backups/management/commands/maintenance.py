from django.core.management.base import BaseCommand, CommandError
from backups.models import BackupFile, FileBackupTask, BackupTask
from scheduler.models import TaskCheck, TaskStatus
import datetime
import arritranco.settings as settings
import sys
from optparse import make_option


class Command(BaseCommand):
    args = ''
    help = 'Clean the TaskChecks and BackupFile'
    option_list = BaseCommand.option_list + (
        make_option('--verbose',
                    dest='verbose',
                    action='store_true',
                    default=False,
                    help='verbose output'),
        make_option('--dry-run',
                    dest='dry',
                    action='store_true',
                    default=False,
                    help="dry run dosn't make changes"
        )
    )

    def handle(self, *args, **options):
        try:

            if options.get('verbose', False):
                self.stdout.write('Deleting backupFiles : ')
                for bkpfile in BackupFile.objects.exclude(deletion_date__isnull=True).filter(
                        deletion_date__lt=(datetime.datetime.now() -
                                           datetime.timedelta(days=settings.BACKUP_FILE_TIME_TO_DELETE))):
                    self.stdout.write('(original date:%s), (deletion date:%s), (file name:%s)' %
                                      (bkpfile.original_date, bkpfile.deletion_date, bkpfile.original_file_name))

            if not options.get('dry', False):
                BackupFile.objects.exclude(deletion_date__isnull=True).filter(
                    deletion_date__lt=(datetime.datetime.now() -
                                       datetime.timedelta(days=settings.BACKUP_FILE_TIME_TO_DELETE))).delete()

            if options.get('verbose', False):
                self.stdout.write('Deleting TaskChecks :')

            for filebackuptask in FileBackupTask.objects.filter(taskcheck__backupfile__isnull=True).distinct():
                for taskcheck in filebackuptask.taskcheck_set.filter(backupfile__isnull=True).distinct():
                    if options.get('verbose', False):
                        self.stdout.write('(task time:%s),(machine:%s),(last run:%s),(description:%s)' %
                                          (taskcheck.task_time, taskcheck.task.machine.fqdn,
                                           taskcheck.task.last_run(), taskcheck.task.description))
                    if not options.get('dry', False):
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
