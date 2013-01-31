# -*- coding: utf-8 -*-
from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.response import Response
from djangorestframework.renderers import DEFAULT_RENDERERS
from django.db.models import Q
from django.conf import settings
from inventory.models import PhysicalMachine, VirtualMachine
from location.models import Room


class BCFG2UPSProperty(ResponseMixin, View):

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        epo_list = {'virtual':[]}
        for room in Room.objects.filter(name__in = settings.UPS_ROOM_NAMES):
            epo_list[room.name] = []
            for m in PhysicalMachine.objects.filter(
                    Q(server__rackserver__rack__room = room)|
                    Q(server__bladeserver__chassis__rack__room = room)
                ):
                epo_list[room.name].append({m.fqdn:m.get_epo_level_display()})
            for m in VirtualMachine.objects.all():
                epo_list['virtual'].append({m.fqdn:m.get_epo_level_display()})
        response = Response(200, epo_list)
        return self.render(response)

class MachinesUPSAssoc(ResponseMixin, View):

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        epo_list = {'virtual':[]}
        for room in Room.objects.filter(name__in = settings.UPS_ROOM_NAMES):
            epo_list[room.name] = []
            for m in PhysicalMachine.objects.filter(
                    Q(server__rackserver__rack__room = room)|
                    Q(server__bladeserver__chassis__rack__room = room),
                    up=True
                ):
                epo_list[room.name].append({m.fqdn:m.get_epo_level_display()})
            for m in VirtualMachine.objects.all():
                epo_list['virtual'].append({m.fqdn:m.get_epo_level_display()})
        response = Response(200, epo_list)
        return self.render(response)

