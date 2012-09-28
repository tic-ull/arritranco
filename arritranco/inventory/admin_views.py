# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView, ListView
from django.conf import settings
from inventory.models import Machine


class ActiveMachinesView(TemplateView):
    template_name = "admin/inventory/machine/active-machines.html"

    def get_context_data(self, room_slug = None, rack_slug = None):
        qs = Machine.objects.filter(up = True)
        return { 'machines': qs, }

class UpdateListView(ListView):
    template_name = "admin/inventory/machine/update_list.html"

    queryset = Machine.objects.filter(up = True).order_by('update_priority', 'up_to_date_date')
