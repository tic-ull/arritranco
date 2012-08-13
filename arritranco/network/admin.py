'''
Created on 25/03/2011

@author: esauro
'''
from django.contrib import admin
from hardware.models import NetworkPort
from models import RoutingZone, NetworkedBuilding, Switch, Network
from models import MACsHistory, ManagementInfo


class NetworkPortInline(admin.TabularInline):
    model = NetworkPort
    extra = 10
    
class SwitchAdmin(admin.ModelAdmin):
    inlines = [NetworkPortInline,
               ]

class NetworkAdmin(admin.ModelAdmin):
    list_display = ('desc','ip','first_ip','last_ip','netmask')
    search_fields = ['desc', 'ip', 'first_ip', 'last_ip']

admin.site.register(Switch, SwitchAdmin)
admin.site.register(MACsHistory)
admin.site.register(RoutingZone)
admin.site.register(NetworkedBuilding)
admin.site.register(ManagementInfo)
admin.site.register(Network, NetworkAdmin)
