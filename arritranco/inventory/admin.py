'''
Created on 25/03/2011

@author: esauro
'''
from django.contrib import admin
from models import Machine, PhysicalMachine, VirtualMachine, OperatingSystem, OperatingSystemType

class MachineAdmin(admin.ModelAdmin):
    list_display = ('fqdn', 'up', 'os', 'start_up', 'update_priority', 'epo_level')
    list_filter = ('up', 'os', 'update_priority', 'epo_level')
    list_editable = ('up','update_priority', 'epo_level')
    date_hierarchy = 'start_up'

class PysicalMachineAdmin(MachineAdmin):
    list_display = ('fqdn', 'server', 'up', 'os', 'start_up', 'update_priority', 'epo_level')
    #list_filter = ('up', 'os', 'update_priority', 'epo_level', 'server__rack__room')
    list_filter = ('up', 'os', 'update_priority', 'epo_level')

admin.site.register(PhysicalMachine, PysicalMachineAdmin)
admin.site.register(VirtualMachine, MachineAdmin)
admin.site.register(OperatingSystem)
admin.site.register(OperatingSystemType)
admin.site.register(Machine, MachineAdmin)
