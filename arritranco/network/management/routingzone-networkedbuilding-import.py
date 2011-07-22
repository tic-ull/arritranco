import csv, sys
from django.db import models
from network.models import RoutingZone
from network.models import NetworkedBuilding
from location.models import Campus

if len(sys.argv) < 4: 
  print "routingzone-networkedbuilding-import.py <importfile.csv>"
  sys.exit(2)

print sys.argv
print len(sys.argv)

reader = csv.reader(open(sys.argv[3], 'rb'), delimiter='\t')
    
cabecera = reader.next()
if (cabecera[0] + cabecera[1]) != "prefixname" :
  print "Input file error"; sys.exit()

for line in reader:
  print line
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
  print "Campus: ", camp, ". Created: ", created
  
  # Create routing zone
  print (_prefix, _name);
  zone, created = RoutingZone.objects.get_or_create(prefix=_prefix,name=_name,bluevlan_prefix=_bluevlan_prefix, public_nets=_public_nets, cajacanarias_nets=_cajacanarias_nets,slug="")
  print "RoutingZone", zone, ". Created: ", created
  
  # Create routing building
  building, created = NetworkedBuilding.objects.get_or_create(name=_name, slug="", area=0, campus=camp, routingzone=zone)
  print "NetworkedBuilding", building, ". Created: ", created

