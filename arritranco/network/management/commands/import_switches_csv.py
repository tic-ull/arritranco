import csv
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from network.models import ManagementInfo, Switch, SWITCH_LEVEL, BACKUP_METHOD_NULL, BACKUP_METHOD_SFTP
from network.models import NetworkedBuilding, RoutingZone
from hardware.models import Rack, Manufacturer, HwType, RackableModel
from location.models import Room

def appenderror(errorlist, line, newproblem, object) :
    _tmp = "ALERT: %s : %s. Line: %s %s %s\n" % (newproblem, object, line[0], line[1], line[3])
    errorlist.append(_tmp)
    print(_tmp) 

def appendcreated(createdlist, iscreated, object) :
    if iscreated :
        _tmp = "Created new %s : %s.\n" % (object.__class__.__name__, object)
        createdlist.append("Created new %s : %s.\n" % (object.__class__.__name__, object)) 
        print(_tmp) 

class Command(BaseCommand):
    args = '<importfile.csv>'
    help = 'Imports Switches from a csv file'
    
    def handle(self, *args, **options):
        _csvfile = ""
        try:
            _csvfile = args[0]
            reader = csv.reader(open(_csvfile, 'rb'), delimiter='\t')
        except :
            raise CommandError("Can't open file %s." % _csvfile)
        
        _cabecera = reader.next()
        if (_cabecera[0] + _cabecera[1] + _cabecera[2]) != "NameTypeGroup" :
            raise CommandError("File format error (header mismatch)")
        
        _errorlist = []
        _createdlist = []
        
        for line in reader:
            _name =  unicode(line[0])
            _modeldesc = unicode(line[1])
            _levelname = unicode(line[2])
            _management_ip = unicode(line[3])
            _buildingprefix = _name[0:1]
            _managementinfoname = "Unmanaged"
            _bkmethod = BACKUP_METHOD_NULL
            _bkusername = ""
            _bkpassword = ""
            _bkconfigfile = ""

            _manufacturername = ""
            _modelname = ""
            _ports = 50
            _manufacturername = "HP"
            if _modeldesc == "HP.Switch.2500" :
                _manufacturername = "HP"
                _modelname = "HP26XX"
                _managementinfoname = "HP Access default"
                _bkmethod = BACKUP_METHOD_SFTP
                _bkusername = ""
                _bkconfigfile = "/cfg/running-config"
            elif _modeldesc == "AlliedTelesis.Switch.8500" :
                _manufacturername = "ATI"
                _modelname = "ATI8524"
                _managementinfoname = "ATI Access default"
                _ports = 24
                _bkusername = "manager"
            else :
                # unknown device. Don't process it
                appenderror(_errorlist, line, "Unknown device type", _modeldesc)
                continue
            
            _level = SWITCH_LEVEL[0][0]
            for l in SWITCH_LEVEL :
                if l[1][0:1] == _levelname[0:1] :
                    _level = l[0]
            
            # get associated NetworkBaseModel, NetworkedBuilding,
            _model = None            
            try :
                _model = RackableModel.objects.get(name=_modelname)
            except :
                pass
                
            if _model == None :
                # get or create Manufacturer
                try :
                    _manufacturer, _created = Manufacturer.objects.get_or_create(name = _manufacturername, slug = " ")
                    appendcreated(_createdlist, _created, _manufacturer)
                except Exception as ex:
                    appenderror(_errorlist, line, "Can't get or create Manufacturer. %s" % ex, _manufacturername)
                    continue            

                # get or create Type
                try :
                    _type, _created = HwType.objects.get_or_create(name = "Switch", slug = " ")
                    appendcreated(_createdlist, _created, _type)
                except Exception as ex:
                    appenderror(_errorlist, line, "Can't get or create Type. %s", ex, "Switch")
                    continue            
                               
                # get or create Model
                _routingzone = None
                try :
                    _model, _created = RackableModel.objects.get_or_create(name = _modelname, units = 1, \
                            type = _type, manufacturer = _manufacturer, slug = " ")                            
                    appendcreated(_createdlist, _created, _model)
                except Exception as ex:
                    appenderror(_errorlist, line, "Can't get or create RackableModel. %s" % ex, _modelname)
                    continue            

            import re
            re_core_sw = re.compile(r"([A-Z]C)[AR]\d$")
            re_dist_sw = re.compile(r"([A-Z][A-Z])([AR])(\d)$")
            re_acce_sw_ati = re.compile(r"([A-Z][A-Z])1(\d)(\d)(.*)")
            re_acce_sw = re.compile(r"([A-Z][A-Z])(\d)(\d)(.*)")
            re_dp_acce_sw = re.compile(r"([A-Z][A-Z])-([^0-9]+)(\d)(\d+)")
            
            _building = ""
            _room_number = ""
            sw_number = ""
            description = ""
            sw_name = _name
            if re_core_sw.match(_name) :
                _building = "CE"
            else :
                match = re_dist_sw.match(_name)
                if match :
                    _building, _room_number, description = match.groups()
                else :
                    match = re_acce_sw_ati.match(_name)
                    if match :
                        _building, _room_number, sw_number, description = match.groups()
                        sw_name = _building + "1" + _room_number + sw_number
                    else :
                        match = re_acce_sw.match(_name)
                        if match :
                            _building, _room_number, sw_number, description = match.groups()
                            sw_name = _building + _room_number + sw_number
                        else :
                            match = re_dp_acce_sw.match(_name)
                            if match :
                                _building, description, _room_number, sw_number = match.groups()
                                sw_name = _building + _room_number + sw_number
                            else :
                                appenderror(_errorlist, line, "Name doen't match any pattern", _name)
                                continue
                        
            #print "SW ", _name, " : ",  sw_name , " --",  _building, _room_number, sw_number, description
            _room_name = _building + _room_number
            _rack_name = "R" + _room_name + "-1"
            
            # get RoutingZone
            _routingzone = None
            try :
                _routingzone = RoutingZone.objects.get(prefix=_building)
            except ObjectDoesNotExist:
                appenderror(_errorlist, line, "RoutingZone prefix prefix no found", _building)
                continue

            # get _building
            _networkbasemodel = None
            try :
                _building = NetworkedBuilding.objects.get(routingzone=_routingzone)
            except ObjectDoesNotExist:
                appenderror(_errorlist, line, "NetworkedBuilding not found", _routingzone)
                continue

            # get or create Room.
            try :
                _room, _created = Room.objects.get_or_create(name = _room_name, building = _building, floor = -9, location = description, slug = " ")
                appendcreated(_createdlist, _created, _room)
            except Exception as ex:
                appenderror(_errorlist, line, "Can't get or create Room. %s" % ex, _room_name)
                continue            
                       
            # get or create Rack. 
            try :
                _rack, _created = Rack.objects.get_or_create(units_number = 42, room = _room, name = _rack_name, slug = " ")
                appendcreated(_createdlist, _created, _rack)
            except Exception as ex:
                appenderror(_errorlist, line, "Can't get or create Rack. %s" % ex, _rack_name)
                continue            
                                                          
            # get or create ManagementInfo
            _managementinfo = None
            try :
                _managementinfo, _created = ManagementInfo.objects.get_or_create( name = _managementinfoname, defaults={ \
                    "defaultports" : _ports, "backupmethod" : _bkmethod, "backupusername" : _bkusername, \
                    "backuppassword" : _bkpassword, "backupconfigfile" : _bkconfigfile, \
                    "recommended_version" : " ", "configtemplate" : " ", "oid" : "1"})
                appendcreated(_createdlist, _created, _model)
            except Exception as ex:
                appenderror(_errorlist, line, "Can't get or create ManagementInfo. %s" % ex, _managementinfoname)
                continue            
                                                
            # Create Switch with...
            #Blank fields: warranty_expires, buy_date
            _sw, _created = Switch.objects.get_or_create(name = sw_name, defaults={ \
                    "model" : _model, "level": _level, "serial_number" : "0", "managementinfo" : _managementinfo,
                    "main_ip" : _management_ip, "ports" : _ports, "slug" : " ", "rack" : _rack, "base_unit" : 0})
            appendcreated(_createdlist, _created, _sw)
#            except Exception as ex:
#                appenderror(_errorlist, line, "Error. Can't create switch", ex)
#                continue
            
        self.stdout.write("\n--CREATED OBJECTS--\n")
        self.stdout.write("\n".join(_createdlist))
        self.stdout.write("\n--ERRORS (Not imported)--\n")
        self.stdout.write("\n".join(_errorlist))
        