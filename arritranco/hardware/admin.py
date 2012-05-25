'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Server, Rack, RackPlace, Chassis, BladeServer, HardDisk, RackServer, UserDevice, NetworkPort

SERVER_LIST_DISPLAY = ('memory', 'processor_type', 'processor_clock', 'processor_number')

class HardDiskInline(admin.TabularInline):
    model = HardDisk
    extra = 2
    
class NetworPortInline(admin.TabularInline):
    model = NetworkPort
    extra = 2
    
class HwAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model_name', 'buy_date', 'warranty_expires')
    date_hierarchy = 'buy_date'
    list_filter = ('model__manufacturer', )

    def model_name(self, obj):
        return obj.model.name
    model_name.short_description = 'model'

class RackableAdmin(HwAdmin):
    list_display = HwAdmin.list_display  + ('rack', )
    list_filter = HwAdmin.list_filter + ('rack__room__building', )

class RackServerAdmin(RackableAdmin):
    list_display = HwAdmin.list_display  + SERVER_LIST_DISPLAY
    inlines = [HardDiskInline, NetworPortInline]  
    raw_id_fields = ('model',)

class BladeServerAdmin(HwAdmin):
    list_display = HwAdmin.list_display  + ('chassis', ) + SERVER_LIST_DISPLAY
    list_filter = HwAdmin.list_filter + ('chassis', 'chassis__rack__room__building' )
    inlines = [HardDiskInline, ]  

class ChasisAdmin(RackableAdmin):
    list_display = RackableAdmin.list_display + ('slots', 'name')

class ServerAdmin(HwAdmin):
    list_display = HwAdmin.list_display + SERVER_LIST_DISPLAY
    inlines = [HardDiskInline, NetworPortInline]  

class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'units_number')
    list_filter = ('room__building', )

admin.site.register(Server, ServerAdmin)
admin.site.register(RackServer, RackServerAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Chassis, ChasisAdmin)
admin.site.register(BladeServer, BladeServerAdmin)
admin.site.register(UserDevice)
admin.site.register(NetworkPort)
