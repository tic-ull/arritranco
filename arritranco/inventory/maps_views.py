# -*- coding: utf-8 -*-
try:
    from djangorestframework.compat import View
    from djangorestframework.mixins import ResponseMixin
    from djangorestframework.response import Response
    from djangorestframework.renderers import DEFAULT_RENDERERS
except:
    pass
from django.db.models import Q
from django.conf import settings
from inventory.models import PhysicalMachine, Machine
from location.models import Room

#FIXME:migrate to new djangorest
# class MapsActiveMachinesProperty(ResponseMixin, View):
#
#     renderers = DEFAULT_RENDERERS
#
#     def get(self, request):
#         machine_map = {'map':[]}
#         for physical_up in PhysicalMachine.objects.filter(up=True):
#             location = physical_up.get_location()
#             if location:
#                 machine_map['map'].append(location)
#
#         response = Response(200, machine_map)
#         return self.render(response)

