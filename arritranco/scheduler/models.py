from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """
        This model define a simple task. You shoud extend it to personalize as much as you wish.
    """
    minute = models.CharField(max_length = 10, help_text = _('Minute (Cron like syntax)'), default = '*')
    hour = models.CharField(max_length = 10, help_text = _('Hour (Cron like syntax)'), default = '*')
    monthday = models.CharField(max_length = 10, help_text = _('Day of moth (Cron like syntax)'), default = '*')
    month = models.CharField(max_length = 10, help_text = _('Month (Cron like syntax)'), default = '*')
    weekday = models.CharField(max_length = 10, help_text = _('Day of week (Cron like syntax)'), default = '*')
    description = models.TextField(help_text = _('Task description'))
    active = models.BooleanField(help_text = _('Is this task active?'), default = True)

    def cron_syntax(self):
        return "%s %s %s %s %s" % (self.minute, self.hour, self.monthday, self.month, self.weekday)

    def __unicode__(self):
        return "%s: %s" % (self.cron_syntax(), self.description)

class TaskCheck(models.Model):
    """
        Model to store all backup ckecks done.
    """
    task = models.ForeignKey(Task)
    task_time = models.DateField(auto_now_add = True, blank=True, null=True, help_text='Task time')
    check_time = models.DateField(auto_now_add = True, blank=True, null=True, help_text='Check time')

    def __unicode__(self):
        return "%s %s" % (self.task.description, self.check_time.strftime('%d-%m-%Y'))

class TaskStatus(models.Model):
    """
        Model to store information about status.
    """
    task_ckeck = models.ForeignKey(TaskCheck)
    time = models.DateTimeField(auto_now_add = True, null=False, help_text='Task status time')
    status = models.CharField(max_length=100, null=False, blank=False, help_text='Status')
    comment = models.TextField(blank=True, null=True, help_text='Comment')

    def __unicode__(self):
        return "%s %s" % (self.time, self.status)
