'''
Created on 25/03/2011

@author: esauro
'''
from django.contrib import admin
from django import forms
from models import Machine, PhysicalMachine, VirtualMachine, OperatingSystem, OperatingSystemType, Interface
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render_to_response, HttpResponseRedirect
import django
from django.template import RequestContext
from network.models import Network

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

# This is a little bit tricky, because nagios app is importing machine model as well, but works ;)
from monitoring.nagios.models import NagiosCheckOpts

import logging
logger = logging.getLogger(__name__)

# Try to import the default name for service interface of a machine
try:
    from settings import DEFAULT_SVC_IFACE_NAME
except ImportError:
    DEFAULT_SVC_IFACE_NAME = None


class NagiosCheckOptsInline(admin.TabularInline):
    model = NagiosCheckOpts


class InterfacesInline(admin.TabularInline):
    model = Interface


class MachineAdmin(admin.ModelAdmin):
    list_display = ('fqdn', 'up', 'os', 'start_up', 'update_priority', 'epo_level', 'network_names')
    list_filter = ('up', 'os', 'update_priority', 'epo_level', 'networks')
#    list_editable = ('up','update_priority','epo_level')
    date_hierarchy = 'start_up'
    search_fields = ('fqdn', 'os__name', 'networks__desc', 'networks__ip')
    inlines = [InterfacesInline, NagiosCheckOptsInline,]
    actions = ['copy_machine']

    def save_model(self, request, obj, form, change):
        """ Control that interface called "DEFAULT_SVC_IFACE_NAME" e.g. "service" is asociated to de fqdn ip"""
        obj.clean()
        obj.save()
        logger.debug("Acabamos de llamar al obj SAVE de MACHINEi %s" % [str(x.id) + " " + str(x) for x in obj.interface_set.all()])
        if obj.up and not obj.get_service_iface():
            svc_iface = obj.build_service_interface() 
            try: # verify that an interface with the fqdn ip exists already then, rename it
                fqdn_iface = obj.interface_set.get(ip=svc_iface.ip)
            except ObjectDoesNotExist:
                fqdn_iface = None
            if obj.get_num_ifaces() == 0 or not fqdn_iface: # If ther is no ifaces, or ther is some but no one with fqdn ip addr, we create the default one
                obj.interface_set.add(svc_iface)
                messages.info(request, _(u'The iface %s has been created bounded to the fqdn of %s' % (obj.get_service_iface(),obj)))
            else: # there is an interface with fqdn ip addr, we rename it to DEFAULT_SVC_IFACE_NAME
                messages.info(request, _(u'The iface founded %s' % fqdn_iface))
                fqdn_iface.name = DEFAULT_SVC_IFACE_NAME
                logger.debug("Llamando al save de la iface: %d - %s " % (fqdn_iface.id, fqdn_iface))
                fqdn_iface.save()
                messages.info(request, _(u'The iface %s has been renamed to default service interface' % obj.get_service_iface()))

    def save_formset(self, request, form, formset, change):
        formset.is_valid()
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Interface):
                logger.debug(instance)
                instance.save()
        formset.save_m2m()
        super(MachineAdmin,self).save_formset(request,form,formset,change)
        logger.debug("DESPUES DE TODOO")

    class CopyMachine(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    # First approach, this is a TODO
    def copy_machine(self, request, queryset):
        """Admin action to copy de basics of a machine."""
        form = None
        if 'apply' in request.POST:
            messages.info(request, _(u'The action has been applied'))
            return HttpResponseRedirect(request.get_full_path())
        if not form: # first call render the form to ask for diferent parametters
            form = self.ConfirmDeleteForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('admin/copy_machine.html', {'machines': queryset,
                                                         'copy_form': form,
                                                        }, context_instance = RequestContext(request))
    copy_machine.short_description = _(u'Copy from selected machine(TODO)') 

class PysicalMachineAdmin(MachineAdmin):
    list_display = ('fqdn', 'server', 'up', 'os', 'start_up', 'update_priority', 'epo_level')
    #list_filter = ('up', 'os', 'update_priority', 'epo_level', 'server__rack__room')
    list_filter = ('up', 'os', 'update_priority', 'epo_level')

class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('ip', 'visible', 'machine', 'network')
    list_filter = ('visible','machine','network')
class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', )
    list_filter = ('type', )


admin.site.register(PhysicalMachine, PysicalMachineAdmin)
admin.site.register(VirtualMachine, MachineAdmin)
admin.site.register(OperatingSystem, OperatingSystemAdmin)
admin.site.register(OperatingSystemType)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(Machine, MachineAdmin)
