'''
Created on 25/12/2010

@author:  rmrodri
'''
from django.contrib import admin
from models import Task, TaskCheck, TaskStatus
from django.db import models
from django import forms
from django.conf import settings

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
    list_filter = ('task', )

    def info(self, obj):
        if 'backups' in settings.INSTALLED_APPS:
        # FIXME: We can have TaskChecks for task's that aren't backups
            return u"Machine: %s" % obj.task.backuptask.machine.fqdn

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

