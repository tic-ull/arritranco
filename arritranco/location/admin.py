'''
Created on 23/12/2010

@author: esauro
'''
from django.contrib import admin
from models import Building, Room, Campus

admin.site.register(Campus)
admin.site.register(Building)
admin.site.register(Room)