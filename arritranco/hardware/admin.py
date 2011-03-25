'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import PhysicalServer, Switch, Rack, Manufacturer, HwModel, HwType, RackPlace, Chasis, BladeServer

admin.site.register(PhysicalServer)
admin.site.register(Switch)
admin.site.register(Rack)
admin.site.register(Manufacturer)
admin.site.register(HwModel)
admin.site.register(HwType)
admin.site.register(RackPlace)
admin.site.register(Chasis)
admin.site.register(BladeServer)