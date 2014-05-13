# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from scheduler.models import TaskStatus
from nsca import NSCA

from django.utils.translation import ugettext_lazy as _
from inventory.models import Machine, PhysicalMachine, VirtualMachine, OperatingSystem
from network.models import Network, IP
from monitoring.models import Responsible
from templatetags.nagios_filters import nagios_safe
from hardware.models import UnrackableNetworkedDevice
from hardware_model.models import HwModel


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
    machines = models.ManyToManyField(Machine)
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
    machines = models.ManyToManyField(Machine, through='NagiosMachineCheckOpts', blank=True, null=True)
    services = models.ManyToManyField(Service, through='NagiosServiceCheckOpts', blank=True, null=True)
    nrpe = models.ManyToManyField(Service, through='sondas.NagiosNrpeCheckOpts', blank=True, null=True,
                                  related_name="nrpeservice")
    unrackable_networked_devices = models.ManyToManyField(UnrackableNetworkedDevice,
                                                          through='NagiosUnrackableNetworkedDeviceCheckOpts',
                                                          blank=True, null=True)
    hwmodels = models.ManyToManyField(HwModel,
                                      through='NagiosHardwarePolicyCheckOpts',
                                      blank=True, null=True)
    slug = models.SlugField()
    description = models.CharField(max_length=400)
    os = models.ManyToManyField("inventory.OperatingSystemType")
    default_contact_groups = models.ManyToManyField("NagiosContactGroup", blank=False, null=False)

    def __unicode__(self):
        return u"%s" % self.name

    def all_machines(self):
        """ Returns all NagiosCheckOpts items which contains machine and options for the NagiosCheck """
        return self.nagioscheckopts_set.filter(machine__up=True).order_by('-machine__os__type__name', 'machine__fqdn')


class NagiosMachineCheckDefaults(models.Model):
    nagioscheck = models.ForeignKey(NagiosCheck)


class NagiosOpts(models.Model):
    """ Check options for a NagiosCheck"""
    check = models.ForeignKey(NagiosCheck)
    options = models.CharField(max_length=500, help_text="Parameter list to a nagios check", null=True, blank=True)
    contact_groups = models.ManyToManyField('NagiosContactGroup')
    
    def __unicode__(self):
        return u"%s " % self.check.name

    class Meta:
        verbose_name = _(u'Asigned nagios check')
        verbose_name_plural = _(u'Asigned nagios checks')

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
    machine = models.ForeignKey(Machine)

    def __unicode__(self):
        return u"%s on machine %s" % (self.check.name, self.machine.fqdn)


class NagiosServiceCheckOpts(NagiosOpts):
    service = models.ForeignKey(Service)

    def __unicode__(self):
        return u"%s on %s" % (self.check.name, self.service.name)

    def service_name(self):
        return str(self.service.name)

    def check_name(self):
        return str(self.check.name)


class NagiosUnrackableNetworkedDeviceCheckOpts(NagiosOpts):
    unrackable_networked_device = models.ForeignKey(UnrackableNetworkedDevice)

    class Meta:
        verbose_name = _(u'Nagios Device Check Ops')

    def __unicode__(self):
        return u"%s on %s" % (self.check.name, self.unrackable_networked_device.name)

    def unrackable_networked_device_name(self):
        return str(self.unrackable_networked_device.name)

    def check_name(self):
        return str(self.check.name)


class NagiosHardwarePolicyCheckOpts(NagiosOpts):
    hwmodel = models.ForeignKey(HwModel)
    excluded_os = models.ManyToManyField(OperatingSystem, null=True, blank=True, help_text="Excluded Os")

    def __unicode__(self):
        return u"%s on %s" % (self.check.name, self.hwmodel.name)

    def hwmodel_name(self):
        return str(self.hwmodel.name)

    def check_name(self):
        return str(self.check.name)


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
    machine = kwargs['instance']
    contact = NagiosContactGroup.objects.get(name=settings.DEFAULT_NAGIOS_CG)
    if not NagiosMachineCheckOpts.objects.filter(machine=machine).count():
        for nch in NagiosMachineCheckDefaults.objects.all():
            nchopt = NagiosMachineCheckOpts.objects.create(machine=machine, check=nch.nagioscheck)
            nchopt.contact_groups.add(contact)
            nchopt.save()

post_save.connect(propagate_status, sender=TaskStatus)
post_save.connect(assign_default_checks, sender=Machine)
post_save.connect(assign_default_checks, sender=PhysicalMachine)
post_save.connect(assign_default_checks, sender=VirtualMachine)
