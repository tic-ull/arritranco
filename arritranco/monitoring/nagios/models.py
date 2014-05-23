# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from scheduler.models import TaskStatus
from nsca import NSCA
from django.utils.translation import ugettext_lazy as _
from network.models import Network, IP
from monitoring.models import Responsible
from templatetags.nagios_filters import nagios_safe
from hardware.models import UnrackableNetworkedDevice
from hardware_model.models import HwModel
from django.core.exceptions import ValidationError


NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

HUMAN_TO_NAGIOS = {
    'Ok': NAGIOS_OK,
    'ok': NAGIOS_OK,
    'bien': NAGIOS_OK,
    'yes': NAGIOS_OK,
    'Warning': NAGIOS_WARNING,
    'Critical': NAGIOS_CRITICAL,
    'Unknown': NAGIOS_UNKNOWN,
}


class Service(models.Model):
    name = models.CharField(max_length=255)
    ip = models.ForeignKey(IP)
    machines = models.ManyToManyField("inventory.Machine")
    date = models.DateField()

    def __unicode__(self):
        return u"%s" % self.name

    def machines_names(self):
        machines_list = ""
        for machine in self.machines.all():
            machines_list = machines_list + " " + str(machine.fqdn)
        return machines_list

    def responsibles(self):
        """ String with all responsibles for notification on nagios """
        groups = set()
        for servicecheckops in self.nagiosservicecheckopts_set.all():
            for cg in servicecheckops.contact_groups.all():
                groups.add(cg.ngcontact)
        return ", ".join(groups)


class NagiosCheck(models.Model):
    """ This represent a nagios check """
    name = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    default_params = models.TextField(help_text="Default params for this check", blank=True, null=True)
    machines = models.ManyToManyField("inventory.Machine", through='NagiosMachineCheckOpts', blank=True, null=True)
    services = models.ManyToManyField(Service, through='NagiosServiceCheckOpts', blank=True, null=True)
    nrpe = models.ManyToManyField(Service, through='sondas.NagiosNrpeCheckOpts', blank=True, null=True,
                                  related_name="nrpeservice")
    unrackable_networked_devices = models.ManyToManyField(UnrackableNetworkedDevice,
                                                          through='NagiosUnrackableNetworkedDeviceCheckOpts',
                                                          blank=True, null=True)
    #hwmodels = models.ManyToManyField(HwModel,
    #                                  through='NagiosHardwarePolicyCheckOpts',
    #                                  blank=True, null=True)
    slug = models.SlugField()
    description = models.CharField(max_length=400)
    os = models.ManyToManyField("inventory.OperatingSystemType")
    default_contact_groups = models.ManyToManyField("NagiosContactGroup", blank=False, null=False)

    def __unicode__(self):
        return u"%s" % self.name

    def all_machines(self):
        """ Returns all NagiosCheckOpts items which contains machine and options for the NagiosCheck """
        return self.nagioscheckopts_set.filter(machine__up=True).order_by('-machine__os__type__name', 'machine__fqdn')

    def default_contact_groups_csv(self):
        return ",".join([i.ngcontact for i in self.default_contact_groups.all()])

    def os_csv(self):
        return ",".join([i.name for i in self.os.all()])


class NagiosMachineCheckDefaults(models.Model):
    nagioscheck = models.ForeignKey(NagiosCheck)

    class Meta:
        verbose_name = _(u'Machine Default Check')
        verbose_name_plural = _(u'Machine Default Checks')


class NagiosOpts(models.Model):
    """ Check options for a NagiosCheck"""
    check = models.ForeignKey(NagiosCheck)
    options = models.CharField(max_length=500, help_text="Parameter list to a nagios check", null=True, blank=True)
    contact_groups = models.ManyToManyField('NagiosContactGroup')
    
    def __unicode__(self):
        return u"%s " % self.check.name

    def get_ngcontact_groups(self):
        """ Returns the contactcroup comaseparated line for the nagios conf """
        return ", ".join([x.ngcontact for x in self.contact_groups.all()])
    get_ngcontact_groups.short_description = _(u'Contact groups assigned')
    get_ngcontact_groups.admin_order_field = 'contact_groups'

    def params(self):
        if self.options is None or self.options == "":
            return self.check.default_params
        return self.options

    def contact_group_all_csv(self):
        contact_groups_csv = ""
        for contact_group in self.contact_groups.all():
            contact_groups_csv = contact_groups_csv + contact_group.ngcontact + ","
        return contact_groups_csv[0:len(contact_groups_csv) - 1]

    def get_full_check(self):
        if self.options is None or self.options == "":
            return self.check.command + self.check.default_params
        else:
            return self.check.command + self.options


class NagiosMachineCheckOpts(NagiosOpts):
    """ Check options for a NagiosCheck on a specific machine, oid's, ports etc.. """
    machine = models.ForeignKey("inventory.Machine")

    class Meta:
        verbose_name = _(u'Machine Check')
        verbose_name_plural = _(u'Machine Checks')

    def __unicode__(self):
        return u"%s on machine %s" % (self.check.name, self.machine.fqdn)

    def clean(self):
        if NagiosMachineCheckOpts.objects.filter(check=self.check,
                                                 machine=self.machine).exclude(pk=self.pk):
            raise ValidationError('Error check in machine repited')


class NagiosServiceCheckOpts(NagiosOpts):
    service = models.ForeignKey(Service)

    class Meta:
        verbose_name = _(u'Service Check')
        verbose_name_plural = _(u'Service Checks')

    def __unicode__(self):
        return u"%s on %s" % (self.check.name, self.service.name)

    def service_name(self):
        return str(self.service.name)

    def check_name(self):
        return str(self.check.name)

    def clean(self):
        if NagiosServiceCheckOpts.objects.filter(check=self.check,
                                                 service=self.service).exclude(pk=self.pk):
            raise ValidationError('Error check in service repited')


class NagiosUnrackableNetworkedDeviceCheckOpts(NagiosOpts):
    unrackable_networked_device = models.ForeignKey(UnrackableNetworkedDevice)

    class Meta:
        verbose_name = _(u'Device Check')
        verbose_name_plural = _(u'Device Checks')

    def __unicode__(self):
        return u"%s on %s" % (self.check.name, self.unrackable_networked_device.name)

    def unrackable_networked_device_name(self):
        return str(self.unrackable_networked_device.name)

    def check_name(self):
        return str(self.check.name)

    def clean(self):
        if NagiosUnrackableNetworkedDeviceCheckOpts.objects.filter(check=self.check,
                                                                   unrackable_networked_device=self.unrackable_networked_device).exclude(pk=self.pk):
            raise ValidationError('Error check in device repited')


class NagiosHardwarePolicyCheckOpts(NagiosOpts):
    hwmodel = models.ManyToManyField(HwModel)
    excluded_os = models.ManyToManyField("inventory.OperatingSystem", null=True, blank=True, help_text="Excluded Os")

    class Meta:
        verbose_name = _(u'Hardware Policy Check')
        verbose_name_plural = _(u'Hardware Policy Checks')

    def __unicode__(self):
        hwNames = ",".join([i.name for i in self.hwmodel.all()])
        return u"%s on %s" % (self.check.name, hwNames)

    def hwmodels_names(self):
        return ",".join([i.name for i in self.hwmodel.all()])

    def check_name(self):
        return str(self.check.name)

    def clean(self):
        HwPolicys = NagiosHardwarePolicyCheckOpts.objects.filter(check=self.check).exclude(pk=self.pk)
        for HwPolicy in HwPolicys:
            for hwmodel in self.hwmodel.all():
                if HwPolicy.hwmodel.filter(pk=hwmodel.pk):
                    raise ValidationError('Error check in hardware %s repited' % hwmodel.name)


class NagiosContactGroup(Responsible):
    """ A nagios concatc group to recieve alerts """
    ngcontact = models.CharField(_(u"Group name"), max_length=100)

    def delete(self, *args, **kwargs):
        """ Check first if there are checks assigned to the contact """
        if NagiosMachineCheckOpts.objects.filter(contact_groups__in=(self,)):
            return False
        else:
            super(NagiosContactGroup, self).delete(*args, **kwargs)
            return True

    def __unicode__(self):
        return u"%s (nagios: %s)" % (self.name, self.ngcontact)


class NagiosNetworkParent(models.Model):
    """ Find parents for nagios hosts """
    network = models.ForeignKey(Network)
    parent = models.CharField(max_length=500, help_text="Parent nagios host for this network", null=False, blank=False)
    
    def __unicode__(self):
        return u"%s is parent for net %s" % (self.parent, self.network)

    class Meta:
        verbose_name = _(u'Nagios network parent')
        verbose_name_plural = _(u'Nagios network parents')

    @staticmethod
    def get_parents_for_host(host):
        nagios_parents = set()
        for iface in host.interface_set.all():
            if iface.network:
                for p in iface.ip.network.nagiosnetworkparent_set.all():
                    nagios_parents.add(p.parent)
        if not nagios_parents:
            return settings.DEFAULT_NAGIOS_HOST_PARENT
        return ', '.join(nagios_parents)


def propagate_status(sender, **kwargs):
    if not settings.PROPAGATE_STATUS_TO_NAGIOS:
        return
    if kwargs['raw']:
        return

    status = kwargs['instance']
    task = status.task_check.task
    if hasattr(task, 'backuptask'):
        nsca = NSCA()
        status_code = HUMAN_TO_NAGIOS[status.status]
        nsca.add_custom_status(task.backuptask.machine.fqdn, nagios_safe(task.description), status_code, status.comment)
        nsca.send()


def assign_default_checks(sender, **kwargs):
    if kwargs['created']:
        machine = kwargs['instance']
        for checkdefault in NagiosMachineCheckDefaults.objects.all():
            if machine.os.type in checkdefault.nagioscheck.os.all():
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

post_save.connect(propagate_status, sender=TaskStatus)


