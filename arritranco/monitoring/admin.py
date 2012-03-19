'''
Created 09/03/2012

@author: alorenzo
'''
from django.contrib import admin
from monitoring.models import Responsible

class ResponsibleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Responsible)

