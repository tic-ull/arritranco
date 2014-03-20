# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status as httpstatus

from django.db.models import Q
from django.conf import settings
from arritranco.inventory.models import PhysicalMachine, VirtualMachine
from arritranco.location.models import Room
from models import HYPERVISOR_HOSTS


class MachinesUPSProperty(APIView):
    """Physical machines ups epo level for bcfg2 properties."""
    def get(self, request, format=None, up=None):
        epo_list = {}
        query = {'up':up} if up else {}
        for room in Room.objects.filter(name__in = settings.UPS_ROOM_NAMES):
            epo_list[room.name] = []
            for m in PhysicalMachine.objects.filter(
                    Q(server__rackserver__rack__room = room)|
                    Q(server__bladeserver__chassis__rack__room = room),
                    **query
                ):
                epo_list[room.name].append({m.fqdn:m.get_epo_level_display()})

        for hypervisor in HYPERVISOR_HOSTS:
            realhyp = hypervisor[1]
            if (realhyp != 'Undefined'):
                epo_list[realhyp] = []
                for m in VirtualMachine.objects.filter(hypervisor = hypervisor[0]):
                    epo_list[realhyp].append({m.fqdn:m.get_epo_level_display()})

        return Response(epo_list, httpstatus.HTTP_200_OK)