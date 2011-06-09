'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Building, Floor, Room, Place, Campus

admin.site.register(Campus)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Place)