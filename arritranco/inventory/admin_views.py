# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic import TemplateView, ListView
from django.conf import settings
from inventory.models import Machine
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import datetime

import logging
logger = logging.getLogger(__name__)


class ActiveMachinesView(TemplateView):
    template_name = "admin/inventory/machine/active-machines.html"

    def get_context_data(self, room_slug = None, rack_slug = None):
        qs = Machine.objects.filter(up = True)
        return { 'machines': qs, }


class UpdateListView(ListView):

    template_name = "admin/inventory/machine/update_list.html"
    queryset = Machine.objects.filter(up = True, os__type__slug = 'Linux').order_by('update_priority','up_to_date_date' )

    def get_context_data(self, **kwargs):
        one_month_ago = datetime.date.today() - datetime.timedelta(days = 30)
        context = super(UpdateListView, self).get_context_data(**kwargs)
        context.update({
                'two_month_ago': one_month_ago,
                'three_month_ago': one_month_ago - datetime.timedelta(days = 2 * 30),
                'sisx_month_ago': one_month_ago - datetime.timedelta(days = 5 * 30),
                'object_list': self.object_list.filter() # Eliminado el filtro para que salgan todas las máquinas en el
                                                         # listado, ya que hay actualizaciones recientes que no saldrian con el filtro
                })

        return context


def filter_by_room(machines, room):
    """
        Returns a qs of machines in a room
    """
    logger.debug("Filtering machines in room %s" % room)
    filtered_machines = []
    for m in machines:
        try:
            pm = m.physicalmachine
        except ObjectDoesNotExist, e:
            # It isn't a physical machine
            continue
        try:
            rs = pm.server.rackserver
            if rs.rack.room.slug == room:
                filtered_machines.append(m)
            continue
        except ObjectDoesNotExist, e:
            # It isn't a rack server
            pass
        try:
            bs = pm.server.bladeserver
            if bs.chassis.rack.room.slug == room:
                filtered_machines.append(m)
        except ObjectDoesNotExist, e:
            # This shouldn't happen
            logger.warning('%s is a physical server but neither rack server nor blade server' % m)
            pass
    return filtered_machines
            
class EPOListView(ListView):
    """
        A machine list ordered by EPO level
    """
    template_name = "admin/inventory/machine/epo_list.html"

    def get_queryset(self):
        qs = Machine.objects.filter(up = True).order_by('epo_level')
        if len(self.args):
            return filter_by_room(qs, self.args[0])
        return qs

    def get_context_data(self, object_list):
        return { 
            'object_list': object_list
            }

