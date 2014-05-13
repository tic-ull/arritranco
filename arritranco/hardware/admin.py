'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Server, Rack, RackPlace, Chassis, BladeServer, HardDisk, RackServer, \
    UnrackableNetworkedDevice, ProcessorType, UnrackableNetworkedDevice

SERVER_LIST_DISPLAY = ('memory', 'processor_type', 'processor_clock', 'processor_number', 'management_ip_addr')


class HardDiskInline(admin.TabularInline):
    model = HardDisk
    extra = 2


class HwAdmin(admin.ModelAdmin):
    search_fields = ['model__name', 'serial_number']
    list_display = ('serial_number', 'model_name', 'buy_date', 'warranty_expires')
    date_hierarchy = 'buy_date'
    list_filter = ('model__manufacturer', )

    def model_name(self, obj):
        return obj.model.name

    model_name.short_description = 'model'


class RackableAdmin(HwAdmin):
    list_display = HwAdmin.list_display + ('rack', )
    list_filter = HwAdmin.list_filter + ('rack__room__building', 'model')


class RackServerAdmin(RackableAdmin):
    list_display = HwAdmin.list_display + SERVER_LIST_DISPLAY
    inlines = [HardDiskInline, ]
    raw_id_fields = ('model',)


class BladeServerAdmin(HwAdmin):
    list_display = HwAdmin.list_display + ('chassis', ) + SERVER_LIST_DISPLAY
    list_filter = ('model__name', 'chassis', 'chassis__rack__room__building' )
    inlines = [HardDiskInline, ]


class ChasisAdmin(RackableAdmin):
    list_display = RackableAdmin.list_display + ('slots', 'name')


class ServerAdmin(HwAdmin):
    list_display = HwAdmin.list_display + SERVER_LIST_DISPLAY
    inlines = [HardDiskInline, ]


class RackAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'units_number')
    list_filter = ('room__building', )


class ProcessorTypeAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model')

class UnrackableNetworkedDeviceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    raw_id_fields = ('main_ip',)


admin.site.register(Server, ServerAdmin)
admin.site.register(RackServer, RackServerAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Chassis, ChasisAdmin)
admin.site.register(BladeServer, BladeServerAdmin)
admin.site.register(ProcessorType)
admin.site.register(UnrackableNetworkedDevice, UnrackableNetworkedDeviceAdmin)
