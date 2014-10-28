# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Task, TaskCheck, TaskStatus
from django.db import models
from django import forms
from django.conf import settings
from monitoring.nagios.models import HUMAN_TO_NAGIOS, NAGIOS_OK, NAGIOS_WARNING, NAGIOS_CRITICAL, NAGIOS_UNKNOWN
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext as _

from django.utils.html import format_html

class TaskCheckStatusFilter(SimpleListFilter):
    title = (u'Status')

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """Returns a list of tuples."""

        return (
            ('Ok', _('Ok')),
            ('Critical', _(u'Critical')),
            ('Warning', _(u'Warning')),
            ('Unknown', _(u'Unknown')),
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the value provided.

        The value is retrievable via `self.value()`
        """

        if self.value():
            checks = [x.id for x in queryset.filter(last_status__status=self.value())]
            return queryset.filter(id__in=checks)


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
    list_filter = (TaskCheckStatusFilter,)
    inlines = [TaskStatusAdmin, ]
    readonly_fields = ('task_time', 'get_files')
    date_hierarchy = 'task_time'
    #FIXME: Not all task are backup tasks, so adding __backuptask in search fields could be a bit risky
    search_fields = ['task__description', 'task__backuptask__machine__fqdn']

    def info(self, obj):
        if 'backups' in settings.INSTALLED_APPS:
            # FIXME: We can have TaskChecks for tasks that aren't backups
            return u"Machine: %s" % obj.task.backuptask.machine.fqdn

    def get_status(self, obj):
        status = obj.last_status
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
        return '<div style="width:100%%; height:100%%; background-color: %s;font-weight:bold;text-align:center;">%s</div>' % (
            color, status)

    get_status.short_description = u'Last check and status'
    get_status.allow_tags = True

    def get_files(self, obj):
        if obj.backupfile_set.all():
            file_list_plain = '<li>'.join( [ str(i) for i in obj.backupfile_set.all() ] )
            return format_html('<ul><li>' + file_list_plain + '</ul>')
        else:
            return None
    get_files.short_description = u'Related files'
    get_files.allow_tags = True


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

