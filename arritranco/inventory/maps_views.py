# -*- coding: utf-8 -*-

from rest_framework.views import Response, APIView
from rest_framework import status as httpstatus

from django.db.models import Q
from django.conf import settings
from inventory.models import PhysicalMachine, Machine
from location.models import Room


class MapsActiveMachinesProperty(APIView):

    def get(self, request):
        machine_map = {'map':[]}
        for physical_up in PhysicalMachine.objects.filter(up=True):
            location = physical_up.get_location()
            if location:
                machine_map['map'].append(location)

        return Response(machine_map, httpstatus.HTTP_200_OK)

