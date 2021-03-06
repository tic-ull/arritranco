from django.db import models
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from validators import validate_day_of_month, validate_day_of_week, validate_hour, validate_minute, validate_month

import logging
import datetime
from cron import *
from croniter import croniter
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)

class TaskManager(models.Manager):
    def todo(self, start_time=None, end_time=None):
        """List of Tasks to be done in a period of time."""

        if not start_time:
            start_time = datetime.datetime.now()
        if not end_time:
            end_time = datetime.datetime.now() + datetime.timedelta(days=1)
        if start_time > end_time:
            raise ValueError
        queryset = self.model.objects.filter(active=True)

        todo = []
        for t in queryset:
            execution_time = t.next_run(start_time)
            while execution_time < end_time:
                todo.append(t)
                execution_time = t.next_run(execution_time + datetime.timedelta(minutes=1))
        return todo


class Task(models.Model):
    """
        This model define a simple task. You shoud extend it to personalize as much as you wish.
    """
    minute = models.CharField(max_length=10, help_text=_('Minute (Cron like syntax)'), default='0',
                              validators=[validate_minute])
    hour = models.CharField(max_length=10, help_text=_('Hour (Cron like syntax)'), default='0',
                            validators=[validate_hour])
    monthday = models.CharField(max_length=10, help_text=_('Day of moth (Cron like syntax)'), default='*',
                                validators=[validate_day_of_month])
    month = models.CharField(max_length=10, help_text=_('Month (Cron like syntax)'), default='*',
                             validators=[validate_month])
    weekday = models.CharField(max_length=40, help_text=_('Day of week (Cron like syntax)'), default='*',
                               validators=[validate_day_of_week])
    description = models.TextField(help_text=_('Task description'))
    active = models.BooleanField(help_text=_('Is this task active?'), default=True)

    objects = TaskManager()

    def cron_syntax(self):
        return "%s %s %s %s %s" % (self.minute, self.hour, self.monthday, self.month, self.weekday)

    def __unicode__(self):
        return "%s: %s" % (self.cron_syntax(), self.description)

    def _get_croniter_entry(self, start_time):
        return croniter(self.cron_syntax(), start_time)

    def _get_crontab_entry(self):
        return SimpleCrontabEntry(self.cron_syntax())

    def next_run(self, start_time=None):
        if not start_time:
            start_time = datetime.datetime.now()
        #return self._get_crontab_entry().next_run(start_time)
        return self._get_croniter_entry(start_time).get_next(datetime.datetime)

    def last_run(self, start_time=None):
        if not start_time:
            start_time = datetime.datetime.now()
        #return self._get_crontab_entry().prev_run(start_time)
        return self._get_croniter_entry(start_time).get_prev(datetime.datetime)

    def update_status(self, task_time, status, comment=None):
        task_check, created = TaskCheck.objects.get_or_create(task=self, task_time=task_time)
        if created:
            task_check.save()
        task_check.update_status(status, comment)

    def get_status(self, d=None):
        if d is not None:
            task_check = get_object_or_404(TaskCheck, task=self, task_time=d)
            return task_check.last_status
        task_check = TaskCheck.objects.filter(task=self).order_by('-task_time')
        if len(task_check):
            return task_check[0].last_status
        return None

    get_status.short_description = 'Last check and status'


class TaskCheck(models.Model):
    """
        Model to store all backup ckecks done.
    """
    task = models.ForeignKey(Task)
    task_time = models.DateTimeField(blank=True, null=True, help_text='Task time')
    last_status = models.ForeignKey("scheduler.TaskStatus", help_text='Status', null=True, blank=True, editable=False)

    def __unicode__(self):
        status = ''
        tch_status = self.last_status
        if isinstance(tch_status, TaskStatus):
            status = tch_status.status
        return u"%s %s (%s)" % (self.task.description, self.task_time.strftime('%d-%m-%Y'), status)

    def get_status(self):
        try:
            return self.taskstatus_set.all().order_by('-check_time')[0]
        except IndexError:
            task_status = TaskStatus(check_time=datetime.datetime.now(), status=u'Unknown', comment=u'This task has no status yet.',
                       task_check=self)
            task_status.save()
            return task_status

    def update_status(self, status, comment=None):
        task_status = TaskStatus.objects.create(status=status, comment=comment, task_check=self)
        task_status.save()

    def num_status(self):
        return self.taskstatus_set.count()


class TaskStatus(models.Model):
    """
        Model to store information about status.
    """
    STATUS_CHOICES = (
        ('Ok', 'Ok'),
        ('Warning', 'Warning'),
        ('Critical', 'Critical'),
        ('Unknown', 'Unknown'),
    )

    task_check = models.ForeignKey(TaskCheck)
    check_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text='Check time')
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, null=False, blank=False, help_text='Status')
    comment = models.TextField(blank=True, null=True, help_text='Comment')

    def __unicode__(self):
        return "%s %s" % (self.check_time.strftime('%d-%m-%Y %H:%M:%S'), self.status)


def update_status(sender, instance, **kwargs):
    logger.info("llamando update status taskstatus: %s" % instance)
    instance.task_check.last_status = instance.task_check.get_status()
    instance.task_check.save()

post_save.connect(update_status, sender=TaskStatus, dispatch_uid="update_status")
