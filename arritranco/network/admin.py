'''
Created on 25/03/2011

@author: esauro
'''
from django.contrib import admin
from hardware.models import NetworkPort
from models import RoutingZone, NetworkedBuilding, Switch
from models import MACsHistory, ManagementInfo


class NetworkPortInline(admin.TabularInline):
    model = NetworkPort
    extra = 10
    
class SwitchAdmin(admin.ModelAdmin):
    inlines = [NetworkPortInline,
               ]

admin.site.register(Switch, SwitchAdmin)
admin.site.register(MACsHistory)
admin.site.register(RoutingZone)
admin.site.register(NetworkedBuilding)
admin.site.register(ManagementInfo)


