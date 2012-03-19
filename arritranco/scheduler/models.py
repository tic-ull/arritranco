from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
import datetime
from cron import *


class Task(models.Model):
    """
        This model define a simple task. You shoud extend it to personalize as much as you wish.
    """
    minute = models.CharField(max_length = 10, help_text = _('Minute (Cron like syntax)'), default = '*')
    hour = models.CharField(max_length = 10, help_text = _('Hour (Cron like syntax)'), default = '*')
    monthday = models.CharField(max_length = 10, help_text = _('Day of moth (Cron like syntax)'), default = '*')
    month = models.CharField(max_length = 10, help_text = _('Month (Cron like syntax)'), default = '*')
    weekday = models.CharField(max_length = 40, help_text = _('Day of week (Cron like syntax)'), default = '*')
    description = models.TextField(help_text = _('Task description'))
    active = models.BooleanField(help_text = _('Is this task active?'), default = True)

    def cron_syntax(self):
        return "%s %s %s %s %s" % (self.minute, self.hour, self.monthday, self.month, self.weekday)

    def __unicode__(self):
        return "%s: %s" % (self.cron_syntax(), self.description)

    def _get_crontab_entry(self):
        return SimpleCrontabEntry(self.cron_syntax())

    def next_run(self, start_time = None):
        if not start_time:
            start_time = datetime.datetime.now()
        return self._get_crontab_entry().next_run(start_time)

    def last_run(self, start_time = None):
        if not start_time:
            start_time = datetime.datetime.now()
        return self._get_crontab_entry().prev_run(start_time)

    @staticmethod
    def todo(start_time = None, end_time = None, queryset = None):
        '''
            Tasks to be done in a period of time.
        '''
        if not start_time:
            start_time = datetime.datetime.now()
        if not end_time:
            end_time = datetime.datetime.now() + datetime.timedelta(days = 1)
        if start_time > end_time:
            raise ValueError
        if not queryset:
            queryset = Task.objects.all()

        todo = []
        for t in queryset:
            execution_time = t.next_run(start_time)
            while execution_time < end_time:
                todo.append((t, execution_time))
                execution_time = t.next_run(execution_time + datetime.timedelta(minutes = 1))
        return todo

    def update_status(self, task_time, status, comment = None):
        task_check, created = TaskCheck.objects.get_or_create(task = self, task_time = task_time)
        if created:
            task_check.save()
        task_check.update_status(status, comment)

    def get_status(self, d = None):
        if d is not None:
            task_check = get_object_or_404(TaskCheck, task = self, task_time = d)
            return task_check.get_status()
        task_check = TaskCheck.objects.filter(task = self).order_by('-task_time')
        if len(task_check):
            return task_check[0].get_status()
        return None
    get_status.short_description = 'Last check and status'

class TaskCheck(models.Model):
    """
        Model to store all backup ckecks done.
    """
    task = models.ForeignKey(Task)
    task_time = models.DateTimeField(blank=True, null=True, help_text='Task time')

    def __unicode__(self):
        status = ''
        if isinstance(self.get_status(), TaskStatus):
            status = self.get_status().status
        return u"%s %s (%s)" % (self.task.description, self.task_time.strftime('%d-%m-%Y'), status)


    def get_status(self):
        try:
            return self.taskstatus_set.all().order_by('-check_time')[0]
        except IndexError:
            return u'Unknown'

    def update_status(self, status, comment = None):
        task_status = TaskStatus.objects.create(status = status, comment = comment, task_check = self)
        task_status.save()

    def num_status(self):
        return self.taskstatus_set.count()

class TaskStatus(models.Model):
    """
        Model to store information about status.
    """
    task_check = models.ForeignKey(TaskCheck)
    check_time = models.DateTimeField(auto_now_add = True, blank=True, null=True, help_text='Check time')
    status = models.CharField(max_length=100, null=False, blank=False, help_text='Status')
    comment = models.TextField(blank=True, null=True, help_text='Comment')

    def __unicode__(self):
        return "%s %s" % (self.check_time.strftime('%d-%m-%Y %H:%M:%S'), self.status)
