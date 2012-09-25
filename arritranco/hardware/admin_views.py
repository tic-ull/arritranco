# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from django.conf import settings
from location.models import Room


class RoomRackView(TemplateView):
    template_name = "admin/hardware/rack/room-rack.html"

    def get_context_data(self):
        return { 'rooms': Room.objects.all().order_by('building'), }

