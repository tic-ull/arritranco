# -*- coding: utf-8 -*-
from django.http import Http404
from django.views.generic import TemplateView
from models import FileBackupTask
from models import TSMBackupTask
from models import R1BackupTask
from inventory.models import Machine
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
import datetime

class BackupGridList(TemplateView):
    template_name = "admin/backups/filebackuptask/grid_list.html"


    def get_context_data(self):
    	list_of_backups = {}
    	for mchn in Machine.objects.filter( up = True ):
 		list_of_backups[mchn.fqdn] = {}
   		list_of_backups[mchn.fqdn]['fqdn'] = mchn.fqdn
                list_of_backups[mchn.fqdn]['R1Soft'] = ''
                list_of_backups[mchn.fqdn]['TSM'] = ''
                list_of_backups[mchn.fqdn]['Sistemas'] = 'NOT_OK'
                list_of_backups[mchn.fqdn]['Datos'] = ''
                list_of_backups[mchn.fqdn]['Databases'] = ''
     		for fbt in FileBackupTask.objects.filter( active = True, machine=mchn.id):
   	           if fbt.machine.fqdn == mchn.fqdn:
			if fbt.bckp_type == 1:
   		          list_of_backups[mchn.fqdn]['Datos'] = 'OK'
			if fbt.bckp_type == 2:
   		          list_of_backups[mchn.fqdn]['Databases'] = 'OK'
			if fbt.bckp_type == 3:
   		          list_of_backups[mchn.fqdn]['Sistemas'] = 'OK'
   
                   if TSMBackupTask.objects.filter(machine=mchn.id):
                        list_of_backups[mchn.fqdn]['TSM'] = 'OK'
   
                   if R1BackupTask.objects.filter(machine=mchn.id):
                        list_of_backups[mchn.fqdn]['R1Soft'] = 'OK'
			
				
	return {'list_of_backups':list_of_backups}
 	



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
            f = {'checker_':self.request.GET['checker']}
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

