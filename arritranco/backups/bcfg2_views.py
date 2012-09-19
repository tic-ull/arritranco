# -*- coding: utf-8 -*-
from djangorestframework.compat import View
from djangorestframework.mixins import ResponseMixin
from djangorestframework.response import Response
from djangorestframework.renderers import DEFAULT_RENDERERS
from django.conf import settings
import datetime
from models import FileBackupTask
from inventory.models import Machine


class BCFG2BackupProperty(ResponseMixin, View):

    renderers = DEFAULT_RENDERERS

    def get(self, request):
        list_of_tasks = {}
        for m in Machine.objects.filter(up = True):
            task_for_machine = {}
            for fbt in FileBackupTask.objects.filter(active = True, machine = m).order_by('bckp_type'):
                bckp_type = fbt.get_bckp_type_display().lower()
                if bckp_type not in task_for_machine:
                    task_for_machine[bckp_type] = []
                data = {
                        'description':fbt.description,
                        'minutes':fbt.minute,
                        'hours':fbt.hour,
                        'doms': fbt.monthday,
                        'months':fbt.month,
                        'dows':fbt.weekday,
                        'server': fbt.checker_fqdn,
                        'path': fbt.directory,
                    }
                if fbt.extra_options:
                    for l in fbt.extra_options.split('\n'):
                        pieces = l.split('=', 2)
                        if len(pieces) > 1:
                            data[pieces[0]] = pieces[1]
                task_for_machine[bckp_type].append(data)
            list_of_tasks[m.fqdn] = task_for_machine

        response = Response(200, list_of_tasks)
        return self.render(response)
