# coding: utf8
from django.db import models
from hardware.models import Server
from network.models import Network
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from django.utils.translation import ugettext_lazy as _

from socket import gethostbyname, gethostbyaddr
from django.core.urlresolvers import reverse

import re
import IPy

# Try to import the default name for service interface of a machine
try:
    from settings import DEFAULT_SVC_IFACE_NAME
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

HYPERVISOR_HOSTS = (
    (0, _(u'Undefined')),
    (1, _(u'VM Ware')),
    (2, _(u'Kernel Virtual Machine')), 
)
KVM_HYPERVISOR = 2

UPS_CHOICES = (
    (0, 'Sin UPS'),
    (1, 'UPS1 Tarj.1'),
    (2, 'UPS1 Tarj.2'),
    (3, 'UPS2 Tarj.1'),
    (4, 'UPS2 Tarj.2'),
    (5, 'UPS VMware'),
    (70,'UPS Etsii'),
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
        gethostbyname(value)
    except:
        raise ValidationError, _(u'The fqdn name u entered is not resoluble, please enter a valid one')

def clean_ip(value):
    """ Check valid IPv4 addr """
    try:
        ip = IPy.IP(value)
    except ValueError:
        raise ValidationError,  _(u'You must provide a valid IPv4 address e.g.: 10.119.70.0')


class Machine(models.Model):
    """
        Maquina Software
    """
    fqdn = models.CharField( max_length = 255, unique = True)
    description = models.TextField(blank = True, null = True)
    up = models.BooleanField('Up', default = False, help_text = _(u'Is this machine up?'))
    #responsable = models.ForeignKey(Responsable, blank=True, null=True, verbose_name='Responsable',
    #    help_text='Datos de contacto del responsable del servicio.')
    #propietario = models.ForeignKey(Propietario, blank=True, null=True)
    # Software
    os = models.ForeignKey(OperatingSystem, blank = True, null = True)
    
#    cacti = models.IntegerField(blank=True, null=True, help_text=_(u'The cacti id for host.'))
#    nagios = models.CharField(max_length=100, blank=True, help_text='Nagios name')
    start_up = models.DateField(_(u'start up'), blank = True, null = True)
    update_priority = models.IntegerField(_(u'Update priority'), choices = UPDATE_PRIORITY, default = 30)
#   fecha_ultima_actualizacion = models.DateField('Actualizada', blank=True, null=True)
    # UPS
    # Prioridades de actualizaciones
    epo_level = models.IntegerField(_(u'EPO Level'), choices = EPO_LEVELS, default = 0)    
    networks = models.ManyToManyField(Network, help_text = _(u'Networks where machine is coneccted through his interfaces'), through = 'Interface')
    def __unicode__(self):
        return u"%s" % (self.fqdn)

#    def save(self, *args, **kwargs):
#        print "SAVE DE MACHINE"
#        super(Machine,self).save(*args,**kwargs)
    def clean(self):
        """ Clean fields only when we need to """
        if self.up:
            clean_fqdn(self.fqdn)

    def get_admin_url(self):
        return reverse('admin:inventory_machine_change',args=(self.id,))

    def resolveip(self):
        """ Return DNS ip for the fqdn if it is resoluble """
        try:
            ip = gethostbyname(self.fqdn)
        except:
            ip = None
        return ip

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
        print "Mirando machine %s" % self
        try:
            service_interface = self.interface_set.get(name=DEFAULT_SVC_IFACE_NAME)
            service_ip = service_interface.ip
        except ObjectDoesNotExist:
            service_ip = '127.0.0.1'
        return service_ip

    def responsibles(self):
        """ String with all responsibles for notification on nagios """
        groups = []
        for co in self.nagioscheckopts_set.all():
            for cg in co.contact_groups.all():
                groups.append(cg.name)
        return ", ".join(groups)

    def network_names(self):
        """ Network names where machine is conected to """
        networks = []
        link = '<a href=\"%s\"> %s </a>'
        for net in self.networks.all().distinct():
            networks.append(link % (net.get_admin_url(),net.desc))
        return ", ".join(networks)

    def has_upsmon(self):
        """Returns if this machine should have upsmon or not."""
        try:
            vm = self.virtualmachine
        except: 
            vm = None
        if vm:
            if vm.hypervisor == KVM_HYPERVISOR:
                return True
            else:
                return not (vm.epo_level in [20,30])
        else:
            return True


    def build_service_interface(self):
        """Returns an Interface with the values of the default service interface for de machine instance.
           
           - This function assumes that the fqdn name is resoluble.
        """
        iface = Interface(
                    machine = self,
                    ip = self.resolveip(),
                    hwaddr = '00:00:00:00:00:00',
                    name = DEFAULT_SVC_IFACE_NAME,
                    visible = True,
                    )
        return iface

    network_names.short_description = _(u'Networks')
    network_names.allow_tags = True

class Interface(models.Model):
    """ Model to represent a machine network interface """
    machine = models.ForeignKey(Machine)
    name = models.CharField(help_text = _(u'Itentified name for the interface'), max_length = 50)
    ip = models.IPAddressField(help_text = _(u'Interface IP v4 address'), validators = [clean_ip])
    hwaddr = models.CharField(help_text = _(u'Mac / Hardware address of the interface'), max_length = 17, validators = [clean_hwaddr])
    visible = models.BooleanField(help_text = _(u'Whether the interface and IP are visible through the network'), default = False)
    network = models.ForeignKey(Network, null = True, blank = True,editable = False)

    class Meta:
        ordering = ['id']
    
    def __unicode__(self):
        return u"%s (%s)  <%s>" % (self.name, self.ip, "UP" if self.visible else "DOWN")

    def save(self, *args, **kwargs):
        """ Assigning the net to which this interface belongs to. """
        
        ip = IPy.IP(self.ip).int()
        nets =  Network.objects.filter(first_ip_int__lte = ip, last_ip_int__gte = ip).order_by('size')
        if nets:
            print "Hay net y la asignamos %s" % nets[0]
            self.network = nets[0]
            print "Ahora self network: %s" % self.network
        super(Interface,self).save(*args,**kwargs)
        print "SAVE DE INTERFACCE DATOS: %d - %s" % (self.id,self)
        print "Despues del super self network: %s" % self.network


class VirtualMachine(Machine):
    """ Machine with no real hardware running on a virtual server like VMWare, KVM or whatever """
    hypervisor = models.IntegerField(_(u'Hypervisor host'), choices = HYPERVISOR_HOSTS, default = 0)    
    processors = models.IntegerField(_(u"Number of processors"), default = 1)
    memory = models.DecimalField('GB RAM', max_digits=15, decimal_places=3, blank=True, null=True)
    total_disks_size = models.DecimalField(_(u"GB"), max_digits=15, decimal_places=3, blank=True, null=True)

class PhysicalMachine(Machine):
    """ Machine with real hardware """
    server = models.ForeignKey(Server, verbose_name=_(u'Server'))
    ups = models.IntegerField(blank=False, help_text=_('Connected UPS'), choices=UPS_CHOICES, default=0)

