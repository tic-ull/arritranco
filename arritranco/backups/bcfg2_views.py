# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from bcfg2_serializers import Bcfg2BackupPropertySerializer
from rest_framework import status as httpstatus
from rest_framework.views import Response

from models import FileBackupTask
from inventory.models import Machine


class BCFG2BackupProperty(APIView):
    """Returns BCFG2 properties on desired format(xml,json,yaml..)."""
    def get(self, request, format=None):
        list_of_tasks = {}
        for m in Machine.objects.filter(up=True):
            task_for_machine = {}
            for fbt in FileBackupTask.objects.filter(active=True, machine=m).order_by('bckp_type'):
                bckp_type = fbt.get_bckp_type_display().lower()
                if bckp_type not in task_for_machine:
                    task_for_machine[bckp_type] = []
                data = Bcfg2BackupPropertySerializer(fbt).data
                task_for_machine[bckp_type].append(data)
            list_of_tasks[m.fqdn] = task_for_machine

        return Response(list_of_tasks, httpstatus.HTTP_200_OK)
