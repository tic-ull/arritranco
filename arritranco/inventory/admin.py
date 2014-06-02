# coding: utf-8
'''
Created on 25/03/2011

@author: esauro
'''
import random

from django import forms
from models import Machine, PhysicalMachine, VirtualMachine, OperatingSystem, OperatingSystemType, Interface
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.forms import ModelForm, Form
from django.conf import settings

# This is a little bit tricky, because nagios app is importing machine model as well, but works ;)
from monitoring.nagios.admin import NagiosMachineCheckOptsInline
from backups.models import FileBackupTask, BackupTask, FileBackupTaskTemplate, FileBackupProductTemplate, \
    FileBackupProduct
import datetime

import logging

logger = logging.getLogger(__name__)

# Try to import the default name for service interface of a machine
try:
    from settings import DEFAULT_SVC_IFACE_NAME
except ImportError:
    DEFAULT_SVC_IFACE_NAME = None


class InterfacesInline(admin.TabularInline):
    model = Interface
    raw_id_fields = ('ip',)


class ManagementIPFilter(SimpleListFilter):
    title = (u'Management Ip')

    parameter_name = 'management ip'

    def lookups(self, request, model_admin):
        return (
            ("with ip", _(u'with ip')),
            ("without ip", _(u'without ip'))
        )

    def queryset(self, request, queryset):
        if self.value():
            machines = None
            if self.value() == "with ip":
                machines = queryset.exclude(server__management_ip=None)
            else:
                machines = queryset.filter(server__management_ip=None)
            return queryset.filter(id__in=machines)


class MachineAdmin(admin.ModelAdmin):
    list_display = ('fqdn', 'up', 'os', 'start_up', 'update_priority', 'epo_level', 'network_names')
    list_filter = ('up', 'os', 'update_priority', 'epo_level')
    date_hierarchy = 'start_up'
    search_fields = ('fqdn', 'os__name')
    inlines = [InterfacesInline, NagiosMachineCheckOptsInline, ]
    actions = ['copy_machine', 'update_machine', 'set_default_checks', 'apply_backupfile']

    def set_default_checks(self, request, queryset):
        """Admin action to set default checks"""
        from monitoring.nagios.models import NagiosMachineCheckDefaults, NagiosMachineCheckOpts, \
            NagiosContactGroup, NagiosCheck

        contact = NagiosContactGroup.objects.get(name=settings.DEFAULT_NAGIOS_CG)
        for machine in queryset:
            for checkdefault in NagiosMachineCheckDefaults.objects.all():
                if (not machine.nagiosmachinecheckopts_set.filter(check=checkdefault.nagioscheck)) and \
                                machine.os.type in checkdefault.nagioscheck.os.all():
                    if checkdefault.nagioscheck.slug == "nut":
                        if machine.has_upsmon():
                            machineCheckOpts = NagiosMachineCheckOpts()
                            machineCheckOpts.check = checkdefault.nagioscheck
                            machineCheckOpts.machine = machine
                            machineCheckOpts.save()
                            for contact_group in checkdefault.nagioscheck.default_contact_groups.all():
                                machineCheckOpts.contact_groups.add(contact_group)
                            machineCheckOpts.save()
                    else:
                        machineCheckOpts = NagiosMachineCheckOpts()
                        machineCheckOpts.check = checkdefault.nagioscheck
                        machineCheckOpts.machine = machine
                        machineCheckOpts.save()
                        for contact_group in checkdefault.nagioscheck.default_contact_groups.all():
                            machineCheckOpts.contact_groups.add(contact_group)
                        machineCheckOpts.save()

        messages.info(request, "%d machine have been set with the default checks" % queryset.count())
        return HttpResponseRedirect(request.get_full_path())

    set_default_checks.short_description = _(u'Set default checks')

    def save_related(self, request, form, formsets, change):
        """Control that interface called "DEFAULT_SVC_IFACE_NAME" e.g. "service" is asociated to de fqdn ip

        Take care! this only works under Django >= 1.4

        """
        form.save_m2m()
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)
        # Our custom process starts here
        machine = form.instance
        if machine.up and not machine.get_service_iface():
            svc_iface = machine.build_service_interface()
            try:
                # Verify that an interface with the fqdn ip already exists, then rename it
                fqdn_iface = machine.interface_set.get(ip=svc_iface.ip)
            except ObjectDoesNotExist:
                fqdn_iface = None
            if machine.get_num_ifaces() == 0 or not fqdn_iface:
                # If there is no ifaces, or ther is some but no one with fqdn
                # ip addr, we create the default one
                machine.interface_set.add(svc_iface)
                messages.info(request, u'The iface %s has been created bounded to the fqdn of %s' % (
                    machine.get_service_iface(), machine))
            else:
                # There is an interface with fqdn ip addr, we rename it to DEFAULT_SVC_IFACE_NAME
                messages.info(request, _(u'The iface founded %s' % fqdn_iface))
                fqdn_iface.name = DEFAULT_SVC_IFACE_NAME
                logger.debug("Calling Interface Save method: %d - %s " % (fqdn_iface.id, fqdn_iface))
                fqdn_iface.save()
                messages.info(request, _(
                    u'The iface %s has been renamed to default service interface' % machine.get_service_iface()))

    class CopyMachineForm(forms.Form):
        fqdn = forms.CharField(max_length=255)
        description = forms.CharField(widget=forms.Textarea)
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    # First approach, this is a TODO
    def copy_machine(self, request, queryset):
        """Admin action to copy de basics of a machine."""
        form = None
        if 'apply' in request.POST:
            messages.info(request, _(u'The action has been applied'))
            return HttpResponseRedirect(request.get_full_path())
        if not form:  # first call render the form to ask for diferent parametters
            form = self.CopyMachineForm(initial=
                                        {
                                            '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME),
                                            'fqdn': queryset[0].fqdn,
                                            'description': queryset[0].fqdn,
                                        }
            )
        return render_to_response('admin/copy_machine.html', {'machines': queryset,
                                                              'copy_form': form,
        }, context_instance=RequestContext(request))

    copy_machine.short_description = _(u'Copy from selected machine(TODO)')

    def update_machine(self, request, queryset):
        """ Admin action to set update date to now"""
        for machine in queryset:
            machine.up_to_date_date = datetime.date.today()
            machine.save()
        messages.info(request, _(u'%s machines has been updated' % (queryset.count())))

    update_machine.short_description = _(u'Machine up to date')

    class BackupFileForm(Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        filebackup = forms.ModelChoiceField(FileBackupTaskTemplate.objects.all())

    def apply_backupfile(self, request, queryset):
        """Admin action to aply a system backup by default."""
        form = None
        if 'apply' in request.POST:
            machineDates = request.session["machineDate"]
            filebackuptemplate = FileBackupTaskTemplate.objects.get(pk=request.POST["filebackup"])
            for machineDate in machineDates:
                machine = Machine.objects.get(fqdn=machineDate["machine"])
                if machine.os in filebackuptemplate.os.all() and machine.up:
                    filebackup = FileBackupTask()
                    filebackup.active = True
                    filebackup.bckp_type = filebackuptemplate.bckp_type
                    filebackup.checker_fqdn = filebackuptemplate.checker_fqdn
                    filebackup.days_in_hard_drive = filebackuptemplate.days_in_hard_drive
                    filebackup.description = filebackuptemplate.name + " para " + machine.fqdn
                    filebackup.directory = filebackuptemplate.directory % {"fqdn": machineDate["machine"]}
                    dt = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0)) + datetime.timedelta(minutes=filebackuptemplate.duration)
                    filebackup.duration = dt.time()
                    filebackup.hour = machineDate["hour"]
                    filebackup.monthday = machineDate["mothday"]
                    filebackup.minute = random.randint(0, 59)
                    filebackup.extra_options = filebackuptemplate.extra_options
                    filebackup.machine = machine
                    filebackup.max_backup_month = filebackuptemplate.max_backup_month
                    filebackup.weekday = "*"
                    filebackup.save()
                    for filebackupproducttemplate in FileBackupProductTemplate.objects.filter(file_backup_task_template=filebackuptemplate):
                        fileBackupProduct = FileBackupProduct()
                        fileBackupProduct.end_seq = filebackupproducttemplate.end_seq
                        fileBackupProduct.file_backup_task = filebackup
                        fileBackupProduct.file_pattern = filebackupproducttemplate.file_pattern
                        fileBackupProduct.start_seq = filebackupproducttemplate.start_seq
                        fileBackupProduct.variable_percentage = fileBackupProduct.variable_percentage
                        fileBackupProduct.save()
                else:
                    messages.error(request, _(u"No se puedo aplicar backup en %s") % machine.fqdn)

            messages.info(request, _(u'The action has been applied'))

            return HttpResponseRedirect(request.get_full_path())
        if not form:  # first call render the form to ask for diferent parametters
            #date = {mothdate:{"nbackups":x,"hours":[nbackpus ...]} ...}
            date = {}
            for mothday in xrange(1, 27):
                hours = {}
                for hour in xrange(0, 7):
                    hours[hour] = FileBackupTask.objects.filter(monthday=mothday,
                                                                hour=hour).count() + FileBackupTask.objects.filter(
                        monthday=mothday, hour="0" + str(hour)).count()

                date[mothday] = {"nbackups": FileBackupTask.objects.filter(monthday=mothday).count(),
                                 "hours": hours}

            # machineDate = [{"machine": machine.fqdn, "mothday": x, "hour": y},  ...]

            machineDate = []

            for machine in queryset:

                minNBackupsDay = min([date[mothday]["nbackups"] for mothday in xrange(1, 27)])
                day = -1
                for i in xrange(1, 27):
                    if date[i]["nbackups"] == minNBackupsDay:
                        day = i
                        break
                #FIXME
                # con muchas maquinas aveces da 0 cuando ha de dar 1
                minNBackupsHour = min([i for i in date[day]["hours"]])
                hour = -1
                for i in xrange(0, 7):
                    if minNBackupsHour == date[day]["hours"][i]:
                        hour = i
                        break

                machineDate.append({"machine": machine.fqdn, "mothday": day, "hour": hour})

                date[day]["nbackups"] += 1
                date[day]["hours"][hour] += 1
                pass

            form = self.BackupFileForm(initial={
                '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME),
            })

            request.session["machineDate"] = machineDate

            return render_to_response('admin/inventory/machine/systembackup.html',
                                      {"form": form,
                                       "action": "apply_backupfile",
                                       "machineDate": machineDate},
                                      context_instance=RequestContext(request))

    apply_backupfile.short_description = _(u'Apply backup file template')


class PysicalMachineAdmin(MachineAdmin):
    list_display = (
        'fqdn', 'server_link', 'ip_link', 'get_warranty_expires', 'up', 'os', 'start_up', 'update_priority', 'epo_level')
    list_filter = ('up', 'os', 'update_priority', 'epo_level', ManagementIPFilter)
    search_fields = ('fqdn', 'server__model__name', 'os__name')

    def server_link(self, obj):
        return "<a href=%s>%s<a/>" % (obj.get_server_admin_url(),
                                      str(obj.server))

    server_link.short_description = u'Server'
    server_link.allow_tags = True

    def ip_link(self, obj):
        return "<a href=https://%s>%s<a/>" % (obj.server.management_ip_addr(),
                                              obj.server.management_ip_addr())

    ip_link.short_description = u'Management ip'
    ip_link.allow_tags = True


class VirtualMachineAdmin(MachineAdmin):
    list_display = ('fqdn', 'hypervisor', 'up', 'os', 'start_up', 'update_priority', 'epo_level')
    list_filter = ('hypervisor', 'up', 'os', 'update_priority', 'epo_level')
    list_editable = ('hypervisor',)


class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('ip_addr', 'visible', 'machine', 'network')
    list_filter = ('visible', 'machine')


class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )
    list_filter = ('type', )


admin.site.register(PhysicalMachine, PysicalMachineAdmin)
admin.site.register(VirtualMachine, VirtualMachineAdmin)
admin.site.register(OperatingSystem, OperatingSystemAdmin)
admin.site.register(OperatingSystemType)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Machine, MachineAdmin)


