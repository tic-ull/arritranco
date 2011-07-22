'''
Created on 25/03/2011

@author: esauro
'''
from django.contrib import admin
from models import Machine, PhysicalMachine, VirtualMachine, OperatingSystem, OperatingSystemType

admin.site.register(PhysicalMachine)
admin.site.register(VirtualMachine)
admin.site.register(OperatingSystem)
admin.site.register(OperatingSystemType)
admin.site.register(Machine)