from django.core.management.base import BaseCommand, CommandError
from arritranco.location.models import *
from arritranco.hardware_model.models import *
from arritranco.hardware.models import *
from arritranco.inventory.models import *
import json
import string

class Command(BaseCommand):
    args = "location_data hardware_data"
    help = "Import the location info in a JSON from all style to new one"
    
    def _parse_file(self, data, model_list):
        result = {}
        for model in model_list:
            result[model] = {}
        for obj in data:
            for model in model_list:
                if obj['model'] == model:
                    result[model][obj['pk']] = obj['fields']
                    
        return result
    
    def _update_ref(self, data, key, old, new):
        for item in data.values():
            if item[key] == old:
                item[key] = new
    
    def handle(self, *args, **options):
        location_data = json.load(open(args[0], "r"))
        hardware_data = json.load(open(args[1], "r"))
        inventario_data = json.load(open(args[2], "r"))
        
        # First app is location
        # First we gather info from the json 
        campus = dict(((10, 'Anchieta'),
                       (20, 'Central'),
                       (30, 'Guajara'),
                       (40, 'OTROS'),
                     ))

        parse_data = self._parse_file(location_data, ['inmuebles.edificio', 'inmuebles.cuarto'])
        rooms = parse_data['inmuebles.cuarto']
        buildings = parse_data['inmuebles.edificio']
        
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
            self._update_ref(rooms, 'edificio', pk, new_obj)
                   
        for room in rooms.values():
            new_obj, created = Room.objects.get_or_create(name = room['nombre'],
                                                          building = room['edificio'],
                                                          floor = room['numero_planta'],
                                                          location = room['localizacion'],
                                                          slug = room['nombre'],
                                                          )  
        # End location import
        
        # Start hardware and servers import
        # Old inventory had one app for hardware models and hardware. We'll start importing models staff
        parse_data = self._parse_file(hardware_data, ['hardware.fabricante', 'hardware.tipohardware', 'hardware.modelohw', 'hardware.armario', 'hardware.hardware'])
        manufacturers = parse_data['hardware.fabricante']
        hardware_type = parse_data['hardware.tipohardware']
        hardware_model = parse_data['hardware.modelohw']
        racks = parse_data['hardware.armario']
        hardwares = parse_data['hardware.hardware']
        inventory_parse_data = self._parse_file(inventario_data, ['inventario.servidor', 'inventario.modeloprocesador', 'inventario.procesador', 'inventario.discoduro', 'inventario.sistemaoperativo', 'inventario.maquina'])
        servers = inventory_parse_data['inventario.servidor']
        processors_models = inventory_parse_data['inventario.modeloprocesador']
        processors = inventory_parse_data['inventario.procesador']
        hard_disks = inventory_parse_data['inventario.discoduro']
        operating_systems = inventory_parse_data['inventario.sistemaoperativo']
        machines = inventory_parse_data['inventario.maquina']
        
        for pk,manufacturer in manufacturers.items():
            new_obj, created = Manufacturer.objects.get_or_create(name = manufacturer['nombre'],
                                               slug = manufacturer['nombre'])
            self._update_ref(hardware_model, 'fabricante', pk, new_obj)
                                    
        for pk,hardwaretype in hardware_type.items():
            new_obj,created = HwType.objects.get_or_create(name = hardwaretype['nombre'],
                                         slug = hardwaretype['nombre'])
            self._update_ref(hardware_model, 'tipohardware', pk, new_obj)
        
        for pk,model in hardware_model.items():
            new_obj,created = HwModel.objects.get_or_create(name = model['nombre'],
                                                            slug = model['nombre'],
                                                            manufacturer = model['fabricante'],
                                                            type = model['tipohardware'],
                                                            )
            self._update_ref(hardwares, 'modelo', pk, new_obj)
        
        for pk,rack in racks.items():
            room = Room.objects.get(name = rooms[rack['cuarto']]['nombre'], building = rooms[rack['cuarto']]['edificio'])
            new_obj,created = Rack.objects.get_or_create(name = rack['nombre'],
                                                         slug = rack['nombre'],
                                                         room = room,
                                                         units_number = 42)
            
            self._update_ref(hardwares, 'armario', pk, new_obj)
        
        proc_manufacturer = {0: 'Intel',
                             1: 'AMD',
                             2: 'IBM',
                             3: 'SUN',
                             }
        for i in proc_manufacturer.values():
            Manufacturer.objects.get_or_create(name = i, slug = i)
        
        for pk,processor_type in processors_models.items():
            manufacturer = Manufacturer.objects.get(name = proc_manufacturer[processor_type['fabricante']])
            new_obj,created = ProcessorType.objects.get_or_create(manufacturer = manufacturer,
                                                            model = processor_type['modelo']
                                                            )
            
            self._update_ref(processors, 'modelo', pk, new_obj)
            
        processor_units = {}
        for p in processors.values():
            if processor_units.has_key(p['servidor']):
                processor_units[p['servidor']] += 1
            else:
                processor_units[p['servidor']] = 1
            
        for pk,processor in processors.items():
            hardwares[processor['servidor']]['processor_type'] = processor['modelo']
            hardwares[processor['servidor']]['processor_clock'] = processor['reloj']
            hardwares[processor['servidor']]['processor_number'] = processor_units[processor['servidor']] 
    
        for pk,hardware in hardwares.items():
            if hardware['modelo'] is None:
                continue
            if hardware['modelo'].type.name == 'Chasis blade':
                if not hardware['u_inicial']:
                    hardware['u_inicial'] = -1
                CHASIS_CHOICES = {'JWHMF1J': {'name': 'A', 'slots': 10},
                                  '88TRN1J': {'name': 'B', 'slots': 10},
                                  '33S652J': {'name': 'C', 'slots': 10},
                                  '480752J': {'name': 'D', 'slots': 10},
                                  'FT1WM3J': {'name': 'E', 'slots': 16},
                                  '6M70P3J': {'name': 'F', 'slots': 16},
                                  'HF3244J': {'name': 'G', 'slots': 16},
                          }
                kwargs = dict(model = hardware['modelo'],
                               serial_number = hardware['no_serie'],
                               rack = hardware['armario'],
                               base_unit = hardware['u_inicial'],
                               warranty_expires = hardware['caducidad_garantia'],
                               buy_date = hardware['fecha_compra'],
                               )
                chasis = CHASIS_CHOICES[hardware['no_serie']]
                Chassis.objects.get_or_create(name = chasis['name'],
                                             slug = chasis['name'],
                                             slots = chasis['slots'],
                                             **kwargs                  
                                         )

        for pk,hardware in hardwares.items():

            if hardware['modelo'] is None:
                continue
            if hardware['modelo'].type.name == 'Servidor Rack' or hardware['modelo'].type.name == 'Servidor blade':
                servidor = servers[pk]
                if not hardware['armario']:
                    hardware['armario'] = Rack.objects.get(pk = 1)
                if not hardware['u_inicial']:
                    hardware['u_inicial'] = -1
                if not hardware['u_final']:
                    hardware['u_final'] = -1
                
                kwargs = dict(model = hardware['modelo'],
                               serial_number = hardware['no_serie'],
                               rack = hardware['armario'],
                               base_unit = hardware['u_inicial'],
                               warranty_expires = hardware['caducidad_garantia'],
                               buy_date = hardware['fecha_compra'],
                               #units = hardware['u_final'],
                               memory = servidor['memoria'],
                               )
                for key in ('proccesor_type', 'processor_clock', 'processor_units'):
                    if hardware.has_key(key):
                        kwargs[key] = hardware[key]
                if hardware['modelo'].type.name == 'Servidor Rack':
                    #new_obj,created = Server.objects.get_or_create(**kwargs)
                    #print "Hay que enchufar los rack servers que no entran ... %s" % kwargs
                    new_obj,created = RackServer.objects.get_or_create(**kwargs)

                elif hardware['modelo'].type.name == 'Servidor blade':
                    print string.ascii_uppercase[servidor['chasis'] - 1]
                    chasis = Chassis.objects.get(name = string.ascii_uppercase[servidor['chasis'] - 1])
                    kwargs['chassis'] = chasis
                    kwargs['slot_number'] = servidor['chasis_slot']
                    del kwargs['base_unit']
                    #del kwargs['units']
                    del kwargs['rack']
                    new_obj,created = BladeServer.objects.get_or_create(**kwargs)
                self._update_ref(machines, 'servidor', pk, new_obj)
                self._update_ref(hard_disks, 'servidor', pk, new_obj)
                
                
        for pk,hard_disk in hard_disks.items():
            if not isinstance(hard_disk['servidor'], Server):
                continue
            new_obj,created = HardDisk.objects.get_or_create(server = hard_disk['servidor'],
                                                             conn = hard_disk['conn'],
                                                             size = hard_disk['capacidad']
                                                            )
            
        # At this point we have all hardware related things imported. We start with machine staffs
        OS_TYPE = dict(
                      ((1, 'Windows'),
                      (2, 'Linux'),
                      (3, 'Solaris')
                      ))
        for v in OS_TYPE.values():
            OperatingSystemType.objects.get_or_create(name = v, slug= v)
            
        for pk,os in operating_systems.items():
            if not os['familia']:
                continue 
            ostype = OperatingSystemType.objects.get(name = OS_TYPE[os['familia']]) 
            new_obj,created = OperatingSystem.objects.get_or_create(name = os['nombre'],
                                                  slug = os['nombre'],
                                                  type = ostype,
                                                  version = os['act'],
                                                  logo = os['logo'])
            self._update_ref(machines, 'sistema_operativo', pk, new_obj)
            
        for pk,machine in machines.items():
            kwargs = dict(fqdn = machine['nombre'],
                          description = machine['descripcion'],
                          up = machine['en_servicio'],
                          os = machine['sistema_operativo'],
                          start_up = machine['fecha_alta'],
                          update_priority = machine['prioridad_actualizacion'],
                          
                          )
            if machine['virtual']:
                new_obj,created = VirtualMachine.objects.get_or_create(**kwargs)
            else:
                if not  isinstance(machine['servidor'], Server):
                    print "Not importing: ", machine
                    continue
                kwargs['server'] = machine['servidor']
                kwargs['ups'] = machine['ups'] 
                new_obj,created = PhysicalMachine.objects.get_or_create(**kwargs)

