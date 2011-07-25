import csv
from django.core.management.base import BaseCommand, CommandError
from network.models import RoutingZone
from network.models import NetworkedBuilding
from location.models import Campus

class Command(BaseCommand):
    args = '<importfile.csv>'
    help = 'Imports NetworkedBuildings from a csv file. It also creates Campus and RoutingZone if necessary'
        
    def handle(self, *args, **options):
        _csvfile = ""
        try:
            _csvfile = args[0]
            reader = csv.reader(open(_csvfile, 'rb'), delimiter='\t')
        except :
            raise CommandError("Can't open file %s." % _csvfile)
        
        cabecera = reader.next()
        if (cabecera[0] + cabecera[1]) != "prefixname" :
            raise CommandError("File format error (header mismatch)")
        
        for line in reader:
            _prefix =  unicode(line[0])
            _name =  unicode(line[1])
            _bluevlan_prefix = line[2]
            _public_nets = line[3]
            _cajacanarias_nets = line[4]
            _campus = "Central"
            if (line[5] == "A"):
                _campus = "Anchieta"
            elif (line[5] == "S"):
                _campus = "Guajara"
            elif (line[5] == "S"):
                _campus = "Santa Cruz"
            
            # get Campus object
            camp, created = Campus.objects.get_or_create(name=_campus)
            self.stdout.write("Campus: %s. Created: %s\n" % (camp, created))
            
            # Create routing zone
            print (_prefix, _name);
            zone, created = RoutingZone.objects.get_or_create(prefix=_prefix,name=_name, bluevlan_prefix=_bluevlan_prefix, \
                                                              public_nets=_public_nets, cajacanarias_nets=_cajacanarias_nets,slug="")
            self.stdout.write("RoutingZone: %s. Created: %s\n" % (zone, created))
            
            # Create routing building
            building, created = NetworkedBuilding.objects.get_or_create(name=_name, slug="", area=0, campus=camp, routingzone=zone)
            self.stdout.write("NetworkedBuilding: %s. Created: %s\n" % (building, created))
