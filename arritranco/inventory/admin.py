# coding: utf-8
'''
Created on 25/03/2011

@author: esauro
'''

from django import forms
from models import Machine, PhysicalMachine, VirtualMachine, OperatingSystem, OperatingSystemType, Interface
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.forms import ModelForm
from django.conf import settings

# This is a little bit tricky, because nagios app is importing machine model as well, but works ;)
from monitoring.nagios.admin import NagiosMachineCheckOptsInline
from backups.models import FileBackupTask, BackupTask
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
    actions = ['copy_machine', 'update_machine', 'set_default_checks', 'aply_system_backupfile']

    def set_default_checks(self, request, queryset):
        """Admin action to set default checks"""
        from monitoring.nagios.models import NagiosMachineCheckDefaults, NagiosMachineCheckOpts,\
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

    class SystemBackupFileForm(ModelForm):
        class Meta:
            model = FileBackupTask
            fields = ['description', 'active', 'days_in_hard_drive', 'checker_fqdn',
                      'max_backup_month', 'duration', 'extra_options', 'bckp_type']

    def aply_system_backupfile(self, request, queryset):
        """Admin action to copy de basics of a machine."""
        form = None
        if 'apply' in request.POST:
            messages.info(request, _(u'The action has been applied'))
            return HttpResponseRedirect(request.get_full_path())
        if not form:  # first call render the form to ask for diferent parametters
            #date = [{"nbackups":x,"hours":[nbackpus ...]} ...]
            date = {}
            for mothday in xrange(1, 27):
                hours = {}
                for hour in xrange(0, 7):
                    hours[hour] = FileBackupTask.objects.filter(monthday=mothday, hour=hour).count()

                date[mothday] = {"nbackups": FileBackupTask.objects.filter(monthday=mothday).count(),
                                 "hours": hours}

            # machineDate = [{"machine": machine.fqdn, "mothday": x, "hour": y},  ...]

            machineDate = []

            for machine in queryset:
                minNBackupsDay = min([i["nbackups"] for i in date])
                day = [i for i in xrange(1, 27) if FileBackupTask.objects.filter(monthday=i).count() == minNBackupsDay][0]
                minNBackupsHour = min([i for i in date[day]["hours"]])
                hour = [i for i in xrange(0, 7) if FileBackupTask.objects.filter(monthday=day, hour=i).count() == minNBackupsHour][0]

                machineDate.append({"machine": machine.fqdn, "mothday": day, "hour": hour})
                date[day]["nbackups"] += 1
                date[day]["hours"][hour] += 1
                pass

            form = self.SystemBackupFileForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME),
                                                      'description': "",
                                                      'active': True,
                                                      'days_in_hard_drive': "",
                                                      'checker_fqdn': "",
                                                      'max_backup_month': "",
                                                      'duration': "",
                                                      'extra_options': "",
                                                      'bckp_type': BackupTask.SYSTEM_BACKUP
                                                     })
            return render_to_response('admin/inventory/machine/systembackup.html',
                                      {"form": form,
                                       "action": "systembackupfile"},
                                       context_instance=RequestContext(request))

    aply_system_backupfile.short_description = _(u'Aply system backup')

class PysicalMachineAdmin(MachineAdmin):
    list_display = ('fqdn', 'server_link', 'ip_link', 'get_warranty_expires', 'up', 'os', 'start_up', 'update_priority', 'epo_level')
    list_filter = ('up', 'os', 'update_priority', 'epo_level', ManagementIPFilter)

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


