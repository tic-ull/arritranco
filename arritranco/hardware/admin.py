'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import PhysicalServer, Switch, Rack

admin.site.register(PhysicalServer)
admin.site.register(Switch)
admin.site.register(Rack)

