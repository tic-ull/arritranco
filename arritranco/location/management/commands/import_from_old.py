from django.core.management.base import BaseCommand, CommandError
from arritranco.location.models import *
import json

class Command(BaseCommand):
    args = "json_file"
    help = "Import the location info in a JSON from all style to new one"
    
    def handle(self, *args, **options):
        data = json.load(open(args[0], "r"))
        
        # First we gather info from the json 
        campus = dict(((10, 'Anchieta'),
                       (20, 'Central'),
                       (30, 'Guajara'),
                       (40, 'OTROS'),
                     ))
        buildings = {}
        rooms = {}
        for obj in data:
            if obj['model'] == 'inmuebles.edificio':
                buildings[obj['pk']] = obj['fields']
            if obj['model'] == 'inmuebles.cuarto':
                rooms[obj['pk']] = obj['fields']
        
        # Now we insert the info into new models
        for pk,camp in campus.items():
            new_obj, created = Campus.objects.get_or_create(name = camp, slug = camp)
            for building in buildings.values():
                 if building['campus'] == pk:
                     building['campus'] = new_obj
                     
        for pk,building in buildings.items():
            new_obj, created = Building.objects.get_or_create(name = building['nombre'],
                                           slug = building['nombre'],
                                           campus = building['campus'],
                                           area = 1)
            for room in rooms.values():
               if room['edificio'] == pk:
                   room['edificio'] = new_obj
                   
        for room in rooms.values():
            new_obj, created = Room.objects.get_or_create(name = room['nombre'],
                                                          building = room['edificio'],
                                                          floor = room['numero_planta'],
                                                          location = room['localizacion'],
                                                          slug = room['nombre'],
                                                          )    
        
        

