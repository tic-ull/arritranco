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

