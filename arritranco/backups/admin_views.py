# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from models import FileBackupTask
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
import datetime

class BackupGrid(TemplateView):
    template_name = "admin/backups/filebackuptask/grid.html"
    day_width = 1250.0 - 200
    minute_width = day_width / (60 * 24.0)

    def get_offset(self, run_time):
        return (run_time.hour * 60 + run_time.minute + run_time.second / 60.0) * self.minute_width

    def get_width(self, duration):
        if duration is not None:
            return self.get_offset(duration)
        else:
            return (30 * self.minute_width)

    def get_context_data(self):
        midnight = datetime.time(23,59,59)
        list_of_tasks = {}
        f = {}
        if 'checker' in self.request.GET:
            f = {'checker_fqdn':self.request.GET['checker']}
        if 'date' in self.request.GET:
            try:
                today = datetime.datetime.strptime(self.request.GET['date'], '%Y/%m/%d').date()
            except ValueError:
                raise Http404('Invalid date %s fmt: %%Y/%%M/%%D' % self.request.GET['date'])
        else:
            today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        id = 0
        for fbt in FileBackupTask.objects.filter(active = True, machine__up = True, **f):
            last_run = fbt.next_run(datetime.datetime.combine(yesterday, midnight))
            while (last_run.date() == today):
                if fbt.machine.fqdn not in list_of_tasks:
                    list_of_tasks[fbt.machine.fqdn] = []
                list_of_tasks[fbt.machine.fqdn].append({
                    'time':last_run,
                    'duration':fbt.duration,
                    'description':fbt.description,
                    'width': self.get_width(fbt.duration),
                    'offset': 230 + self.get_offset(last_run),
                    'id':id,
                })
                last_run = fbt.next_run(last_run + datetime.timedelta(minutes = 1))
                id += 1
        return {
            'minute_width': self.minute_width,
            'list_of_tasks':list_of_tasks,
            'checker_list':[checker[0] for checker in settings.FILE_BACKUP_CHECKERS]
            }

