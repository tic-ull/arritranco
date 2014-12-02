from django.db import models
from network.models import Network, IP
from hardware.models import RackServer, Rack, BladeServer
from location.models import Room
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import socket
import re
import IPy
from django.db.models.signals import post_save
from monitoring.nagios.models import assign_default_checks

import logging

logger = logging.getLogger(__name__)

# Try to import the default name for service interface of a machine
try:
    from arritranco.settings import DEFAULT_SVC_IFACE_NAME
except ImportError:
    DEFAULT_SVC_IFACE_NAME = None

UPDATE_PRIORITY = (
    (10, _(u'Don\'t worry')),
    (20, _(u'Watch services.')),
    (22, _(u'Watch services. Be careful.')),
    (23, _(u'Be much careful, critical services.')),
    (25, _(u'HA services.')),
    (30, _(u'Not defined. Caution.')),
    (150, _(u'DANGER DO NOT UPDATE!')),
    (160, _(u'DO NOT TOUCH, OUT OF UPDATE CYCLE!')),
    (200, _(u'Depend on third party')),
    (300, _(u'Not applicable')),
)

EPO_LEVELS = (
    (0, _(u'Undefined')),
    (5, _(u'No Service')),
    (10, _(u'No service lost (Service degradation)')),
    (20, _(u'Service Lost. No critical service')),
    (30, _(u'Service Lost. CRITICAL service')),
)

UNDEF_HYPERVISOR = 0
VMWARE_HYPERVISOR = 1
KVM_HYPERVISOR = 2

HYPERVISOR_HOSTS = (
    (UNDEF_HYPERVISOR, 'Undefined'),
    (VMWARE_HYPERVISOR, 'VMWare'),
    (KVM_HYPERVISOR, 'KVM'),
)

UPS_CHOICES = (
    (0, 'Sin UPS'),
    (1, 'UPS1 Tarj.1'),
    (2, 'UPS1 Tarj.2'),
    (3, 'UPS2 Tarj.1'),
    (4, 'UPS2 Tarj.2'),
    (5, 'UPS VMware'),
    (70, 'UPS Etsii'),
    (6, 'No se aplica'),
)

# Create your models here.
class OperatingSystemType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return u"%s" % self.name


class OperatingSystem(models.Model):
    """
        OS
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    type = models.ForeignKey(OperatingSystemType)
    version = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.name, self.version)


def clean_hwaddr(value):
    """ Check the construction of the mac address """
    MAC_RE = r'^([0-9a-fA-F]{2}([:-]?|$)){6}$'
    mac_re = re.compile(MAC_RE)
    if not mac_re.match(value):
        raise ValidationError, _(u'You must enter a valid mac address e.g.: 10:0f:c0:a0:00:b0 or 10-0f-c0-a0-00-b0')


def clean_fqdn(value):
    """ Check fqdn hostname is defined on the DNS zone """
    try:
        socket.gethostbyname(value)
    except:
        raise ValidationError, _(u'The fqdn name u entered is not resoluble, please enter a valid one')

class Machine(models.Model):
    """Software Machine."""
    fqdn = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    up = models.BooleanField('Up', default=False, help_text=_(u'Is this machine up?'))
    os = models.ForeignKey(OperatingSystem)
    start_up = models.DateField(_(u'start up'), blank=True, null=True)
    update_priority = models.IntegerField(_(u'Update priority'), choices=UPDATE_PRIORITY, default=30)
    up_to_date_date = models.DateField(_(u'update date'), blank=True, null=True)
    epo_level = models.IntegerField(_(u'EPO Level'), choices=EPO_LEVELS, default=5)


    class Meta:
        ordering = ['fqdn']
        verbose_name = _('Machine')
        verbose_name_plural = _('Machines')

    def __unicode__(self):
        return u"%s" % (self.fqdn)

    def clean(self):
        """ Clean fields only when we need to """
        if self.up:
            clean_fqdn(self.fqdn)

    def get_admin_url(self):
        return reverse('admin:inventory_machine_change', args=(self.id,))

    def resolveip(self):
        """ Return DNS ip for the fqdn if it is resoluble """
        myip = None

        try:
            ip = socket.gethostbyname(self.fqdn)
            myip, created = IP.objects.get_or_create(addr=ip)
        except socket.gaierror, e:
            # The fqdn is not in the DNS
            logger.info("Unknown DNS name '%s': %s" % (self.fqdn, e))
        except Exception as e:
            logger.exception("Unknown error resolving DNS name for '%s': %s" % (self.fqdn, e))

        return myip

    def get_num_ifaces(self):
        """ Returns the count of interfaces asociated to a machine instance """
        return self.interface_set.all().count()

    def get_service_iface(self):
        """ Returns the interface named DEFAULT_SVC_IFACE_NAME if exists """
        try:
            svc_iface = self.interface_set.get(name=DEFAULT_SVC_IFACE_NAME)
        except ObjectDoesNotExist:
            svc_iface = None
        return svc_iface

    def get_service_ip(self):
        """ Returns the ip of the interface with DEFAULT_SVC_IFACE_NAME name """
        service_ip = ''
        try:
            service_interface = self.interface_set.get(name=DEFAULT_SVC_IFACE_NAME)
            #service_ip = service_interface.ip
        except ObjectDoesNotExist:
            service_ip = '127.0.0.1'
        return service_interface.ip if service_ip == '' else service_ip

    @staticmethod
    def get_by_addr(addr, filter_up=False):
        """
            Returns a machine by a IP or a DNS name.

            addr: addrees or FQDN of the machine.
            filter_up: decide either yes or not wer want only up machines on results.
        """
        try:
            # Search by IP
            if filter_up:
                return Machine.objects.get(interface__ip__addr=addr, up=True)
            else:
                return Machine.objects.get(interface__ip__addr=addr)
        except Machine.DoesNotExist:
            # It's ok, we'll try searching by name
            pass
        except Machine.MultipleObjectsReturned:
            logger.error("Multiple machines with the same IP %s" % addr)
            return None

        try:
            # Search by Name
            if filter_up:
                return Machine.objects.get(fqdn=addr, up=True)
            else:
                return Machine.objects.get(fqdn=addr)
        except Machine.DoesNotExist:
            # It's ok too, our last try will be a reverse DNS search
            pass

        try:
            # FIXME
            # The addr name could have more than one reverse DNS name.
            # In these cases we would iterate by the list of reverse names
            return Machine.objects.get(fqdn=socket.getfqdn(addr), up=True)
        except Machine.DoesNotExist:
            return None

    def responsibles(self):
        """ String with all responsibles for notification on nagios """
        groups = set()
        for co in self.nagiosmachinecheckopts_set.all():
            for cg in co.contact_groups.all():
                groups.add(cg.ngcontact)
        return ", ".join(groups)

    def network_names(self):
        """ Network names where machine is conected to """
        # FIXME
        """networks = []
        link = '<a href=\"%s\"> %s </a>'
        for net in self.networks.all().distinct():
            networks.append(link % (net.get_admin_url(),net.desc))
        return ", ".join(networks)"""
        return ""

    network_names.short_description = _(u'Networks')
    network_names.allow_tags = True

    def has_upsmon(self):
        """Returns if this machine should have upsmon or not."""
        try:
            vm = self.virtualmachine
        except ObjectDoesNotExist:
            return True

        if vm.hypervisor == KVM_HYPERVISOR:
            return True

        # VMware
        return False

    def build_service_interface(self):
        """Returns an Interface with the values of the default service interface for de machine instance.
           
           - This function assumes that the fqdn name is resoluble.
        """
        ip = self.resolveip()
        if not ip:
            return None

        iface = Interface()
        iface.machine = self
        iface.ip = ip
        iface.hwaddr = '00:00:00:00:00:00'
        iface.name = DEFAULT_SVC_IFACE_NAME
        iface.visible = True
        return iface

    def get_nagios_parents(self):
        return 'Router_ccti1'

    def get_all_ips(self):
        ips = [interface.ip for interface in self.interface_set.all()]
        physicalMachine = PhysicalMachine.objects.filter(pk=self.pk)
        if physicalMachine and physicalMachine[0].server.management_ip:
            ips.append(physicalMachine[0].server.management_ip)
        return ips

class Interface(models.Model):
    """ Model to represent a machine network interface """
    machine = models.ForeignKey(Machine)
    name = models.CharField(help_text=_(u'Itentified name for the interface'), max_length=50)
    ip = models.ForeignKey(IP)
    hwaddr = models.CharField(help_text=_(u'Mac / Hardware address of the interface'), max_length=17,
                              validators=[clean_hwaddr])
    visible = models.BooleanField(help_text=_(u'Whether the interface and IP are visible through the network'),
                                  default=False)

    class Meta:
        verbose_name = _('Interface')
        verbose_name_plural = _('Interfaces')

    def __unicode__(self):
        return u"%s (%s)  <%s>" % (self.name, self.ip.addr, "UP" if self.visible else "DOWN")

    def network(self):
        if self.ip.network is None:
            return "No Network"
        return str(self.ip.network)

    def ip_addr(self):
        return self.ip.addr


class VirtualMachine(Machine):
    """ Machine with no real hardware running on a virtual server like VMWare, KVM or whatever """
    hypervisor = models.IntegerField(_(u'Hypervisor host'), choices=HYPERVISOR_HOSTS, default=0)
    processors = models.IntegerField(_(u"Number of processors"), default=1)
    memory = models.DecimalField('GB RAM', max_digits=15, decimal_places=3, blank=True, null=True)
    total_disks_size = models.DecimalField(_(u"GB"), max_digits=15, decimal_places=3, blank=True, null=True)

    class Meta:
        verbose_name = _('Virtual machine')
        verbose_name_plural = _('Virtual machines')


class PhysicalMachine(Machine):
    """ Machine with real hardware """
    server = models.ForeignKey("hardware.Server", verbose_name=_(u'Server'))
    ups = models.IntegerField(blank=False, help_text=_('Connected UPS'), choices=UPS_CHOICES, default=0)

    class Meta:
        verbose_name = _('Physical machine')
        verbose_name_plural = _('Physical machines')

    def get_warranty_expires(self):
        return self.server.warranty_expires

    def get_location(self):
        """ returns location (physical) """
        print "Get location"
        try:
            server = RackServer.objects.get(id=self.server.id)
            room = Room.objects.filter(id=server.rack.room.id)[0]
            location = {'fqdn': self.fqdn, 'rack': server.rack.name, 'room': room.name, 'base_unit': server.base_unit}
        except ObjectDoesNotExist:
            try:
                server = BladeServer.objects.get(id=self.server.id)
                room = Room.objects.get(id=server.chassis.rack.room.id)
                location = {'fqdn': self.fqdn, 'rack': server.chassis.rack.name, 'room': room.name, 'base_unit': server.chassis.base_unit}
            except ObjectDoesNotExist:
                return None
        return location

    def get_management_ip(self):
        if self.server.management_ip is None or self.server.management_ip == "":
            return None
        return self.server.management_ip.addr

    def get_server_admin_url(self):
        return reverse('admin:hardware_server_change', args=(self.server.id,))


post_save.connect(assign_default_checks, sender=Machine)
post_save.connect(assign_default_checks, sender=PhysicalMachine)
post_save.connect(assign_default_checks, sender=VirtualMachine)
