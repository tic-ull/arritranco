from django.core.management.base import BaseCommand, make_option, CommandError
from network.models import Switch

def appenderror(errorlist, line, newproblem, object) :
    _tmp = "ALERT: %s : %s. Line: %s %s %s\n" % (newproblem, object, line[0], line[1], line[3])
    errorlist.append(_tmp)
    print(_tmp) 

def appendcreated(createdlist, iscreated, object) :
    if iscreated :
        _tmp = "Created new %s : %s.\n" % (object.__class__.__name__, object)
        createdlist.append("Created new %s : %s.\n" % (object.__class__.__name__, object)) 
        print(_tmp) 

def backupsw(command, basedir, switch):
    dstfile = "%s/%s.cfg" % (basedir, switch.name)
    backable, errorDesc = switch.backup_config_to_file(destinationfile = dstfile)
    if backable :
        if errorDesc :
            command.stdout.write("\nError backing up %s. %s" % (switch.name, errorDesc))
        else :
            command.stdout.write("\n%s backup OK." % switch.name)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='allswitches', default=False, help="Backup all switches"),
    )    
    args = '<backupfilesbasedirectory> [switch_name]'
    help = 'Backups the configuration of a switch (or all the swiches if --all is specified).'
    
    
    def handle(self, *args, **options):
        allswitches = options.get('allswitches', False)
        if len(args) < 1 :
            raise CommandError('Error. No base directory specified')
        elif (not allswitches) and (len(args) < 2) :
            raise CommandError('Error. No switch name specified')
        basedir = args[0]
        if allswitches :
            for sw in Switch.objects.all() :
                backupsw(self, basedir, sw)
        else :
            # get associated NetworkBaseModel, NetworkedBuilding,
            sw = None            
            try :
                sw = Switch.objects.get(name = args[1])
            except :
                pass

            if sw == None :
                raise CommandError('Error. Switch %s not found' % args[1])
            else :
                backupsw(self, basedir, sw)

            
            
            
            

            

    
