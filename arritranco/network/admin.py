'''
Created on 25/03/2011

@author: esauro
'''
from django.contrib import admin
from models import RoutingZone, NetworkedBuilding, Switch, Network, IP
from models import ManagementInfo
from django.contrib.admin import SimpleListFilter


class NetworkIPFilter(SimpleListFilter):
    title = (u'Network Ip')

    parameter_name = 'Network ip'

    def lookups(self, request, model_admin):
        return ((x.ip, u"%s (%d)" % (x.ip, x.number_of_ips())) for x in Network.objects.all() if (x.number_of_ips() > 0))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(network__ip=self.value())
        return None


class SwitchAdmin(admin.ModelAdmin):
    raw_id_fields = ('main_ip',)
    pass


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('desc', 'ip', 'first_ip', 'last_ip', 'netmask')
    search_fields = ['desc', 'ip', 'first_ip', 'last_ip']


class IPAdmin(admin.ModelAdmin):
    list_display = ('addr', 'network_addr', )
    list_filter = (NetworkIPFilter,)
    search_fields = ['addr',]


admin.site.register(Switch, SwitchAdmin)
admin.site.register(RoutingZone)
admin.site.register(NetworkedBuilding)
admin.site.register(ManagementInfo)
admin.site.register(Network, NetworkAdmin)
admin.site.register(IP, IPAdmin)
