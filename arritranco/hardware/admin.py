'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Server, Rack, RackPlace, Chasis, BladeServer, HardDisk

class HardDiskInline(admin.TabularInline):
    model = HardDisk
    extra = 2
    
class ServerAdmin(admin.ModelAdmin):
    inlines = [HardDiskInline, ]  

admin.site.register(Server, ServerAdmin)
admin.site.register(Rack)
admin.site.register(RackPlace)
admin.site.register(Chasis)
admin.site.register(BladeServer)


