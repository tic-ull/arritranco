'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Server, Switch, Rack, Manufacturer, HwModel, HwType, RackPlace, Chasis, BladeServer, NetworkPort,MACsHistory
from hardware.models import HardDisk, NetworkBaseModel

class HardDiskInline(admin.TabularInline):
    model = HardDisk
    extra = 2
    
class ServerAdmin(admin.ModelAdmin):
    inlines = [HardDiskInline,
               ]
    
class NetworkPortInline(admin.TabularInline):
    model = NetworkPort
    extra = 10
    
class SwitchAdmin(admin.ModelAdmin):
    inlines = [NetworkPortInline,
               ]

admin.site.register(Server, ServerAdmin)
admin.site.register(Switch, SwitchAdmin)
admin.site.register(Rack)
admin.site.register(Manufacturer)
admin.site.register(HwModel)
admin.site.register(HwType)
admin.site.register(RackPlace)
admin.site.register(Chasis)
admin.site.register(BladeServer)
admin.site.register(MACsHistory)
admin.site.register(NetworkBaseModel)