
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import Machine

import json
import datetime


@permission_required('change_machine')
def update_update_date(request, machine_id):
    m = Machine.objects.get(pk=machine_id)
    m.up_to_date_date = datetime.datetime.today()
    m.save()
    return HttpResponseRedirect(reverse('update-list'))

def get_up_machines_by_os(request, req_os):
    machines = [ ]

    result = Machine.objects.filter(up=True, os__name=req_os)
    for m in result:
        machines.append(m.fqdn)

    return HttpResponse(json.dumps(machines))


