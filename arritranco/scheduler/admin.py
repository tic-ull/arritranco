'''
Created on 25/12/2010

@author:  rmrodri
'''
from django.contrib import admin
from models import Task, TaskCheck, TaskStatus
from django.db import models
from django import forms

class TaskStatusAdminForm(forms.ModelForm):

    class Meta:
        STATUS_CHOICES = (
                ('', 'Seleccione un nuevo estado'),
                ('ok', 'ok'),
                ('Error', 'Error')
            ) 
        model = TaskStatus
        widgets = {
            'status': forms.widgets.Select(choices = STATUS_CHOICES),
        }

class TaskStatusAdmin(admin.StackedInline):
    model = TaskStatus
    form = TaskStatusAdminForm
    readonly_fields = ('time', )
    ordering = ('time', )
    extra = 1


class TaskCheckAdmin(admin.ModelAdmin):
    inlines = [ TaskStatusAdmin, ]
    readonly_fields = ('task_time', 'check_time', )

admin.site.register(Task)
admin.site.register(TaskCheck, TaskCheckAdmin)

