# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView, ListView
from django.conf import settings
from inventory.models import Machine
from django.db.models import Q
import datetime


class ActiveMachinesView(TemplateView):
    template_name = "admin/inventory/machine/active-machines.html"

    def get_context_data(self, room_slug = None, rack_slug = None):
        qs = Machine.objects.filter(up = True)
        return { 'machines': qs, }

class UpdateListView(ListView):
    template_name = "admin/inventory/machine/update_list.html"

    queryset = Machine.objects.filter(up = True).order_by('-os__type', 'up_to_date_date','-update_priority' )

    def get_context_data(self, object_list):
        one_month_ago = datetime.date.today() - datetime.timedelta(days = 30)
        return {
                'two_month_ago': one_month_ago,
                'three_month_ago': one_month_ago - datetime.timedelta(days = 2 * 30),
                'sisx_month_ago': one_month_ago - datetime.timedelta(days = 5 * 30),
                'object_list': object_list.filter(Q(up_to_date_date__lte = one_month_ago) | Q(up_to_date_date__isnull = True))
                }
