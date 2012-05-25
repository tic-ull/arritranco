from inventory.models import Machine, OperatingSystem
from backups.models import FileBackupTask, R1BackupTask, TSMBackupTask
from django.shortcuts import render_to_response
from models import NagiosCheck, NagiosCheckOpts
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from helpers.processors import mco2dict

from django.contrib import messages

from django.utils.translation import ugettext_lazy as _

def hosts(request):
    '''
        Nagios hosts config file.
    '''
    template = 'nagios/hosts.cfg'
    context = {}
    context['machines'] = Machine.objects.filter(up = True)
    if 'file' in request.GET:
        response = render_to_response(template, context, mimetype="text/plain")
        response['Content-Disposition'] = 'attachment; filename=%s' % request.GET['file'] 
    else:
        response = render_to_response(template, context, mimetype="text/plain")
    return response



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

def get_checks(request, name):
    """ Render all defined checks of "name" for all machines UP. """
    template = 'nagios/' + name + '_checks.cfg'
    context = {}
    try:
        check = NagiosCheck.objects.get(slug = name)
    except ObjectDoesNotExist: 
        check = None
    if check:
        servers = []
        for machine_check_options in  check.all_machines(): 
            servers.append(mco2dict(machine_check_options))
        context['servers'] = servers
        if 'file' in request.GET:
            filename = name + '_checks.cfg'
            response = render_to_response(template, context, mimetype="text/plain")
            response['Content-Disposition'] = 'attachment; filename=%s' % request.GET['file'] 
        else:
            response = render_to_response(template, context, mimetype="text/plain")
    else:
        response = HttpResponse(u"Check %s does not exist" % name, content_type = "text/plain")
        response.status_code =  404
    return response


def backup_checks(request):
    '''
        Backup checks
    '''
    template = 'nagios/backup_checks.cfg'
    context = {}
    context['backup_file_tasks'] = FileBackupTask.objects.filter(machine__up=True).filter(active=True)
    context['r1soft_tasks'] = R1BackupTask.objects.filter(machine__up=True).filter(active=True)
    context['TSM_tasks'] = TSMBackupTask.objects.filter(machine__up=True).filter(active=True)
    if 'file' in request.GET:
        response = render_to_response(template, context, mimetype="text/plain")
        response['Content-Disposition'] = 'attachment; filename=%s' % request.GET['file'] 
    else:
        response = render_to_response(template, context, mimetype="text/plain")
    return response
