from inventory.models import Machine, OperatingSystem
from backups.models import FileBackupTask, R1BackupTask, TSMBackupTask
from django.shortcuts import render_to_response

def hosts(request):
    '''
        Nagios hosts config file.
    '''
    context = {}
    context['machines'] = Machine.objects.filter(up = True)
    return render_to_response('nagios/hosts.cfg', context, mimetype="text/plain")

def hosts_ext_info(request):
    '''
        nagios extinfo config file
    '''
    l = []
    # FIXME:
    for os in OperatingSystem.objects.filter(type__name__in = ['Linux', 'Windows', 'Solaris']):
        running_machines = os.machine_set.filter(up = True)
        if running_machines.count():
            machines = []
            for m in running_machines:
# FIXME: We need to import ip's from the old tool to improve this a little bit.
#                if m.maquinared_set.filter(visible = True).count():
#                    machines.append(m)
                machines.append(m)
            if len(machines):
                l.append((os.logo, ",".join([m.fqdn for m in machines])))
    context = {"logo_machines": l }
    return render_to_response('nagios/host_ext_info.cfg', context, mimetype="text/plain")

def generic_checks(request, template):
    context = {}
    context['windows_servers'] = Machine.objects.filter(up = True, os__type__name = 'Windows')
    context['linux_servers'] = Machine.objects.filter(up = True, os__type__name = 'Linux')
    context['solaris_servers'] = Machine.objects.filter(up = True, os__type__name = 'Solaris')
    return render_to_response(template, context, mimetype="text/plain")

def backup_checks(request):
    '''
        Backup checks
    '''
    # FIXME: Filter active hosts and active tasks
    context = {}
    context['backup_file_tasks'] = FileBackupTask.objects.all()
    context['r1soft_tasks'] = R1BackupTask.objects.all()
    context['TSM_tasks'] = TSMBackupTask.objects.all()
    return render_to_response('nagios/backup_checks.cfg', context, mimetype="text/plain")

