'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Building, Room, Campus

class RoomAdmin(admin.ModelAdmin):
    search_fields = ['name', 'building__name', 'location']
    list_display = ('name', 'building', 'building', 'floor', 'location')
    list_filter = ('building', )

class BuildingAdmin(admin.ModelAdmin):
    search_fields = ['name', 'campus__name']
    list_display = ('name', 'map_location', 'area', 'campus')
    list_filter = ('campus', )

admin.site.register(Campus)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
