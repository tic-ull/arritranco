
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Machine

import datetime

@permission_required('change_machine')
def update_update_date(request, machine_id):
    m = Machine.objects.get(pk = machine_id)
    m.up_to_date_date = datetime.datetime.today()
    m.save()
    return HttpResponseRedirect(reverse('update-list'))

