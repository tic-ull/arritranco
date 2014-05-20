'''
Created 08/03/2012

@author: alorenzo
'''
from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from django.contrib.admin import SimpleListFilter

from models import NagiosCheck, NagiosMachineCheckOpts, NagiosContactGroup, NagiosNetworkParent, \
    NagiosServiceCheckOpts, NagiosUnrackableNetworkedDeviceCheckOpts, Service, NagiosHardwarePolicyCheckOpts,\
    NagiosMachineCheckDefaults
from inventory.models import Machine
# Try to import the default nagios contact group
try:
    from settings import DEFAULT_NAGIOS_CG
except ImportError:
    DEFAULT_NAGIOS_CG = None


# Custom filter for OS on machine checks

class OsMachineCheckFilter(SimpleListFilter):
    title = (u'Os')

    parameter_name = 'os'

    def lookups(self, request, model_admin):
        """Returns a list of tuples."""

        return (
            ('Solaris', _('Solaris')),
            ('Linux', _(u'Linux')),
            ('Windows', _(u'Windows')),
        )

    def queryset(self, request, queryset):
        """Returns the filtered queryset based on the value provided.

        The value is retrievable via `self.value()`
        """

        if self.value():
            checks = [x.id for x in queryset.filter(machine__os__type__name=self.value())]
            return queryset.filter(id__in=checks)




class NagiosMachineCheckOptsInline(admin.TabularInline):
    model = NagiosMachineCheckOpts

class NagiosServiceCheckOptsInline(admin.TabularInline):
    model = NagiosServiceCheckOpts


class NagiosMachineCheckDefaultsAdmin(admin.ModelAdmin):
    list_display = ('nagioscheck',)
    pass


class NagiosCheckAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'default_params')
    search_fields = ('name',)
    actions = ['set_def_checks']


class NagiosMachineCheckOptsAdmin(admin.ModelAdmin):
    list_display = ('check', 'machine', 'options', 'get_ngcontact_groups')
    list_editable = ('options',)
    search_fields = ('check__name', 'machine__fqdn')
    list_filter = ('contact_groups', 'check',OsMachineCheckFilter)
    filter_horizontal = ('contact_groups',)

    def set_def_checks(self, request, queryset):
        """ Assign default checks to each UP machine we have """
        if not DEFAULT_NAGIOS_CG:
            messages.error(request,
                           _(u'The default nagios contact group should be defined in settings.py: DEFAULT_NAGIOS_CG'))
        else:
            def_cg, created = NagiosContactGroup.objects.get_or_create(ngcontact=DEFAULT_NAGIOS_CG,
                                                                       name='Default group')
            if created:
                def_cg.save()
            def_checks = queryset
            non_def_checks = def_checks.filter(default=False)
            if non_def_checks:
                messages.error(request, _(
                    u'There were some non-default checks selected on the queryset e.g.: %s' % non_def_checks))
            else:
                up_machines = Machine.objects.filter(up=True)
                n_checks = 0
                n_existent_checks = 0
                for c in def_checks:
                    for m in up_machines:
                        try:
                            co = NagiosMachineCheckOpts.objects.get(check=c, machine=m, contact_groups=def_cg)
                        except ObjectDoesNotExist:
                            co = None
                        if co:
                            n_existent_checks += 1
                        else:
                            co = NagiosMachineCheckOpts(check=c, machine=m)
                            co.save()
                            co.contact_groups = (def_cg,)
                            co.save()
                            n_checks += 1
                messages.info(request, u'Created %d nagios checks on %d  UP! machines (%d checks already exists).' % (
                    n_checks, len(up_machines), n_existent_checks))

    set_def_checks.short_description = _(u'Asign selected default checks to all up machines')


class NagiosContactGroupAdmin(admin.ModelAdmin):
    actions = ['delete_contact', ]

    def get_actions(self, request):
        """ Disable delete_selected action to control the delete operation, even in querysets """
        actions = super(NagiosContactGroupAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_contact(self, request, queryset):
        """ Check if there are checks active for a contact, before delete it """
        for contact in queryset:
            if contact.delete():
                messages.info(request, _(u'Deleted contact: %s ' % contact))
            else:
                messages.warning(request,
                                 _(u'Contact %s can not be deleted while having check notifications active' % contact))

    delete_contact.verbose_name = _(u'Delete selected contacts')


class NagiosNetworkParentAdmin(admin.ModelAdmin):
    list_display = ('network', 'parent')


class NagiosServiceCheckOptsAdmin(admin.ModelAdmin):
    search_fields = ['service_name', 'check_name']
    list_display = ('service_name', 'check_name')
    filter_horizontal = ('contact_groups',)


class NagiosUserdeviceCheckOptsAdmin(admin.ModelAdmin):
    search_fields = ['unrackable_networked_device_name', 'check_name']
    list_display = ('unrackable_networked_device_name', 'check_name')
    filter_horizontal = ('contact_groups',)


class NagiosHardwarePolicyCheckOptsAdmin(admin.ModelAdmin):
    search_fields = ['hwmodel_name', 'check_name']
    list_display = ('hwmodel_name', 'check_name')
    filter_horizontal = ('contact_groups',)

class ServiceAdmin(admin.ModelAdmin):
    inlines = [NagiosServiceCheckOptsInline]
    search_fields = ['name', 'machines_names', 'ip']
    list_display = ('name', 'machines_names', 'ip')
    filter_horizontal = ('machines',)
    raw_id_fields = ('ip',)


admin.site.register(NagiosMachineCheckOpts, NagiosMachineCheckOptsAdmin)
admin.site.register(NagiosCheck, NagiosCheckAdmin)
admin.site.register(NagiosContactGroup, NagiosContactGroupAdmin)
admin.site.register(NagiosNetworkParent, NagiosNetworkParentAdmin)
admin.site.register(NagiosServiceCheckOpts, NagiosServiceCheckOptsAdmin)
admin.site.register(NagiosUnrackableNetworkedDeviceCheckOpts, NagiosUserdeviceCheckOptsAdmin)
admin.site.register(NagiosHardwarePolicyCheckOpts, NagiosHardwarePolicyCheckOptsAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(NagiosMachineCheckDefaults, NagiosMachineCheckDefaultsAdmin)

