'''
Created on 25/12/2010

@author:  rmrodri
'''
from django.contrib import admin
from models import Task, TaskCheck, TaskStatus
from django.db import models
from django import forms
from django.conf import settings
from monitoring.nagios.models import HUMAN_TO_NAGIOS, NAGIOS_OK, NAGIOS_WARNING, NAGIOS_CRITICAL, NAGIOS_UNKNOWN

class TaskStatusAdminForm(forms.ModelForm):
#    class Meta:
#        STATUS_CHOICES = (
#                ('', 'Seleccione un nuevo estado'),
#                ('Ok', 'ok'),
#                ('Error', 'Error')
#            ) 
        model = TaskStatus
#        widgets = {
#            'status': forms.widgets.Select(choices = STATUS_CHOICES),
#        }


class TaskStatusAdmin(admin.StackedInline):
    model = TaskStatus
    form = TaskStatusAdminForm
    readonly_fields = ('check_time', )
    ordering = ('check_time', )
    extra = 1


class TaskCheckAdmin(admin.ModelAdmin):
    list_display = ('task', 'task_time', 'num_status', 'get_status', 'info')
    inlines = [ TaskStatusAdmin, ]
    readonly_fields = ('task_time', )
    date_hierarchy = 'task_time'
    search_fields = ['task__description', ]

    def info(self, obj):
        if 'backups' in settings.INSTALLED_APPS:
            # FIXME: We can have TaskChecks for tasks that aren't backups
            return u"Machine: %s" % obj.task.backuptask.machine.fqdn

    def get_status(self, obj):
        status = obj.get_status()
        if isinstance(status, TaskStatus):
            nagios_status = HUMAN_TO_NAGIOS[status.status]
        else:
            nagios_status = NAGIOS_UNKNOWN
        if nagios_status == NAGIOS_OK:
            color = '#BBFEC9'
        elif nagios_status == NAGIOS_WARNING:
            color = 'yellow'
        elif nagios_status == NAGIOS_UNKNOWN:
            color = 'orange'
        elif nagios_status == NAGIOS_CRITICAL:
            color = 'red'
        else:
            color = 'yellow'
        return '<div style="width:100%%; height:100%%; background-color: %s;font-weight:bold;text-align:center;">%s</div>' % (color, status)
    get_status.short_description = u'Last check and status'
    get_status.allow_tags = True


class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'cron_syntax', 'get_status', 'last_run', 'next_run')
    fieldsets = [
        (
            'Recurrence', {
            'fields': ['minute', 'hour', 'monthday', 'month', 'weekday']
            }
        ),
        (
            'Date information', {
            'fields': ['description', 'active']
            }
        ),
    ]

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCheck, TaskCheckAdmin)

