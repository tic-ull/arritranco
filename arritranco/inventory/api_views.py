# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status as httpstatus

from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from inventory.models import PhysicalMachine, VirtualMachine
from location.models import Room
from models import HYPERVISOR_HOSTS, VMWARE_HYPERVISOR, Machine, KVM_HYPERVISOR

# More friendly to work with
HYPERVISOR_DICT = dict(HYPERVISOR_HOSTS)

KVM_HYPERVISOR_STRING = HYPERVISOR_DICT[KVM_HYPERVISOR]

import logging

logger = logging.getLogger(__name__)


class MachinesNutEpoLevel(APIView):
    """Physical machines ups epo level for bcfg2 properties."""

    def get(self, request, format='json'):
        filter = {}
        if not 'fqdn' in request.GET:
            msg = _(u'fqdn required')
            return Response({'msg': 'required fqdn param via GET'}, status=httpstatus.HTTP_400_BAD_REQUEST)
        filter['fqdn'] = request.GET['fqdn']
        filter['up'] = True
        logger.debug("Querying UPS association to machine (filter: %s)" % filter)
        response = {}
        try:
            machine = Machine.objects.get(**filter)
            if hasattr(machine,'virtualmachine'):
                if machine.virtualmachine.hypervisor == VMWARE_HYPERVISOR:
                    return Response({}, httpstatus.HTTP_200_OK)
                elif machine.virtualmachine.hypervisor == KVM_HYPERVISOR:
                    response['cpd'] = KVM_HYPERVISOR_STRING
            else:
                if not response.has_key('cpd'):
                    response['cpd'] = machine.physicalmachine.get_location()['room']
            response['level'] = machine.get_epo_level_display()
        except ObjectDoesNotExist: # No data on the response if machine does not exists or not match the query.
            return Response({}, httpstatus.HTTP_200_OK)
        return Response(response, httpstatus.HTTP_200_OK)
