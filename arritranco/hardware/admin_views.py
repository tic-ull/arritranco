# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from django.conf import settings
from location.models import Room


class RoomRackView(TemplateView):
    template_name = "admin/hardware/rack/room-rack.html"

    def get_context_data(self, room_slug = None, rack_slug = None):
        qs = Room.objects.all()
        if room_slug:
            qs = qs.filter(slug = room_slug)
        return { 'rooms': qs, 'rack_slug': rack_slug}

