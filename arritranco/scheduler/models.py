from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from math import ceil
from datetime import *
import time
import os
from scheduler.scheduler_settings import *



INTERVAL_TYPES = {
    1: ('minutes', 60),
    2: ('hours', 3600),
    3: ('days', 86400),
    4: ('weeks', 604800),
}


STATUS_TYPES = {
    1: 'Queued',
    2: 'Processing',
    3: 'Failed',
    4: 'Completed',
    5: 'Cancelled',
}


class Recurrence(models.Model):
    description     = models.CharField("Description", max_length=50)
    interval        = models.IntegerField(default = 15)
    interval_type   = models.IntegerField(default = 1)


    def next_runtime(self, start_dt):
        current_dt = datetime.now()

        m = INTERVAL_TYPES[self.interval_type][1]

        if self.interval > 0 or start_dt == None:
            current_dt = datetime.now()
            ss = time.mktime(start_dt.timetuple())
            cs = time.mktime(current_dt.timetuple())
            rs = self.interval * m
            nt = time.localtime(ss+(ceil((cs-ss)/rs)*rs))
            next_dt = datetime(nt.tm_year,
                               nt.tm_mon,
                               nt.tm_mday,
                               nt.tm_hour,
                               nt.tm_min,
                               nt.tm_sec)
            return next_dt
        else:
            return start_dt


    def __unicode__(self):
        return self.description


    #class Admin:
    #    list_display = (['description'])
    #    list_filter = (['description'])
    #    pass


class Task(models.Model):
    description     = models.CharField("Description", max_length=50)
    program         = models.CharField("Program", max_length=50)
    longdescription = models.CharField("Long description", max_length=250)
    recurrence      = models.ForeignKey(Recurrence)
    start_datetime  = models.DateTimeField("Start date and time")
    user            = models.ForeignKey(User)


    def __unicode__(self):
        return "Task: " + str(self.id)


    #class Admin:
    #    list_display = ('description',
    #                    'user',
    #                    'program',
    #                    'longdescription',
    #                    'recurrence',)
    #    list_filter = ('description',
    #                   'user')
    #    pass



class Schedule(models.Model):
    task            = models.ForeignKey(Task)
    scheduled_dt    = models.DateTimeField("Scheduled date and time")
    start_dt        = models.DateTimeField("Start date and time", null=True)
    end_dt          = models.DateTimeField("End date and time", null=True)
    status          = models.IntegerField(default = 1)
    message         = models.CharField("Message", max_length=200)


    def status_descr(self):
        "Return a sensible text describing the status"
        return STATUS_TYPES[self.status]


    def start_task(self):
        "Show the current running task as started"
        schedules = Schedule.objects.filter(id = self.id, status = 1)
        for s in schedules:
            s.status = 2
            s.start_dt = datetime.now()
            s.save()
            s.add_log_message("Task start.")


    def failed_task(self):
        "Mark the current running task as failed"
        schedules = Schedule.objects.filter(id = self.id, status = 2)
        for s in schedules:
            s.status = 3
            s.end_dt = datetime.now()
            s.save()
            s.add_log_message("Task failed.")
            self.closeFile('stdout.txt')


    def end_task(self):
        "Finish up the current running task"
        schedules = Schedule.objects.filter(id = self.id, status = 2)
        for s in schedules:
            s.status = 4
            s.end_dt = datetime.now()
            s.save()
            s.add_log_message("Task ended successfully.")
            self.closeFile('stdout.txt')
            # If recurring task, reschedule
            t = Task.objects.get(id = s.task_id)
            r = Recurrence.objects.get(id = t.recurrence_id)
            if r.interval_type <> 0:
                new_datetime = r.next_runtime(s.scheduled_dt)
                newtask = Schedule(task_id = s.task_id, scheduled_dt = new_datetime, status = 1)
                newtask.save()
        else:
            print "Unable to mark task with instance",self.id,"as ended"


    def set_message(self, message):
        "Set a message for the current running task"
        schedules = Schedule.objects.filter(id = self.id, status = 2)
        for s in schedules:
            s.message = message
            s.save()


    def add_log_message(self, message):
        "Add a message to this tasks log."
        l = Log.objects.create(schedule = self,
                                    log = message,
                                    timestamp_dttm = datetime.now()
                                    )
        l.save()


    def createFile(self, filename):
        "Return a filename to use as an export file for the task program."
        f = File.objects.create(schedule = self, filename = filename)
        f.save()
        self.add_log_message("File created: "+filename)
        return f.createFile()


    def closeFile(self, filename):
        "Close the attached file."
        files = File.objects.filter(schedule = self, filename = filename[filename.rfind('/')+1:])
        for f in files:
            f.closeFile()
            self.add_log_message("File closed: "+filename)


    def numberFiles(self):
        "Return the number of files created for the scheduled task"
        return len(File.objects.filter(schedule = self))


    def runnow(self):
        "Set the run time for start when the scheduler awakes.  \
         Please note that the status of the task instance must  \
         be 'queued'. "
        schedules = Schedule.objects.filter(id = self.id, status = 1)
        for s in schedules:
            s.scheduled_dt = datetime.now()
            s.save()


    def reschedule(self):
        "Set the run time for start when the scheduler awakes   \
         to rerun this program after it had failed.             \
         Please note that the status of the task instance must  \
         be 'failed', 'completed' or 'cancelled'. "
        schedules = Schedule.objects.filter(id = self.id, status__in = (3,4,5))
        for s in schedules:
            t = Task.objects.get(id = s.task_id)
            r = Recurrence.objects.get(id = t.recurrence_id)
            if r.interval_type <> 0:
                new_datetime = r.next_runtime(s.scheduled_dt)
                newtask = Schedule(task_id = s.task_id, scheduled_dt = new_datetime, status = 1)
                newtask.save()
            else:
                newtask = Schedule(task_id = s.task_id, scheduled_dt = datetime.now(), status = 1)
                newtask.save()


    def create(self):
        "Schedule a new task identified by the provided task_id."
        tasks = Task.objects.filter(pk = self.task_id)
        for t in tasks:
            self.scheduled_dt = t.start_datetime
            self.save()


    def cancel(self):
        "Cancel this task that was scheduled.                       \
         Please note that the status of the task instance must      \
         be 'scheduled' or 'processing'. Note that this does cancel \
         the task from the scheduler tables, however, it does not   \
         cancel the actual program running. "
        schedules = Schedule.objects.filter(id = self.id, status__in = (1,2))
        for s in schedules:
            s.status = 5
            s.start_dt = datetime.now()
            s.save()


    def delete(self):
        "Delete this task and its related files.                \
         the task must be 'failed', 'cancelled', or 'completed'."
        schedules = Schedule.objects.filter(id = self.id, status__in = (3,4,5))
        for s in schedules:
            files = File.objects.filter(schedule = s)
            if len(files) > 0:
                for f in files:
                    os.remove(f.file())
                os.rmdir(files[0].path())
            super(Schedule, s).delete()
            Log.objects.filter(schedule = self).delete()
            File.objects.filter(schedule = self).delete()


    def __unicode__(self):
        return "Schedule: " + str(self.id)



class Log(models.Model):
    schedule        = models.ForeignKey(Schedule)
    log             = models.CharField("Log line", max_length=250)
    timestamp_dttm  = models.DateTimeField()


    def __unicode__(self):
        return "Log: " + str(self.id) + " - " + str(self.schedule_id)



class File(models.Model):
    schedule        = models.ForeignKey(Schedule)
    filename        = models.CharField("File name", max_length=50)
    filepath        = models.CharField("File path", max_length=250)
    filesize        = models.IntegerField(default = 0)


    def file(self):
        return os.path.join(self.filepath, self.filename)

    def path(self):
        return self.filepath

    def createFile(self):
        dir = SCHEDULER_FILE_ROOT+'/'+str(self.schedule_id)
        try:
            os.makedirs(dir, 0777)
            self.filepath = dir
            self.save()
            return self.file()
        except OSError:
            pass
        return '/dev/null'


    def closeFile(self):
        self.filesize = os.stat(self.file()).st_size
        self.save()


    def __unicode__(self):
        return "File: " + str(self.id)



# --- Newforms Admin Section
from django.contrib import admin

scheduler_admin_site = admin.AdminSite()


class RecurrenceAdmin(admin.ModelAdmin):
    list_display = ('description',)
    list_filter = ('description',)
    ordering = ('description',)
    

class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'program', 'longdescription', 'recurrence',)
    list_filter = ('description', 'user',)
    ordering = ('description',)


scheduler_admin_site.register(Recurrence, RecurrenceAdmin)
scheduler_admin_site.register(Task, TaskAdmin)

