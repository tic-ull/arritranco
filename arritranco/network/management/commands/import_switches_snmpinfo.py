from django.core.management.base import BaseCommand
from network.models import Switch, SWITCH_LEVEL_SNMP

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
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='use_base_manager', default=False,
            help="Backup all switches."),
    )    
    args = '<importfile.csv>'
    help = 'Imports Switches from a csv file'
    
    def handle(self, *args, **options):
        for sw in Switch.objects.all() :
            #_community = [sw.level]
            _ip = sw.main_ip
            self.stdout.write("\n %s - %s - %s : %s" % ( sw.name, _ip, sw.level, SWITCH_LEVEL_SNMP[sw.level]))
        

    
