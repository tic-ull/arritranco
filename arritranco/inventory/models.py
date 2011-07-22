from django.db import models
from hardware.models import Server
from django.utils.translation import ugettext_lazy as _

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
    
class Machine(models.Model):
    """
        Maquina Software
    """
    fqdn = models.CharField( max_length=255)
    description = models.TextField(blank=True, null=True)
    up = models.BooleanField('Up', default = False, help_text=_(u'Is this machine up?'))
    #responsable = models.ForeignKey(Responsable, blank=True, null=True, verbose_name='Responsable',
    #    help_text='Datos de contacto del responsable del servicio.')
    #propietario = models.ForeignKey(Propietario, blank=True, null=True)
    # Software
    os = models.ForeignKey(OperatingSystem, blank=True, null=True)
    
#    cacti = models.IntegerField(blank=True, null=True, help_text=_(u'The cacti id for host.'))
#    nagios = models.CharField(max_length=100, blank=True, help_text='Nagios name')
    start_up = models.DateField(_(u'start up'), blank=True, null=True)
    update_priority = models.IntegerField(_(u'Update priority'), choices=UPDATE_PRIORITY, default=30)
#   fecha_ultima_actualizacion = models.DateField('Actualizada', blank=True, null=True)
    # UPS
    # Prioridades de actualizaciones
    epo_level = models.IntegerField(_(u'EPO Level'), choices=EPO_LEVELS, default=0)    

    def __unicode__(self):
        return u"%s" % (self.fqdn)
    
class VirtualMachine(Machine):
    processors = models.IntegerField(_(u"Number of processors"))
    memory = models.DecimalField('GB RAM', max_digits=15, decimal_places=3, blank=True, null=True)
    total_disks_size = models.DecimalField(_(u"GB"), max_digits=15, decimal_places=3, blank=True, null=True)

class PhysicalMachine(Machine):
    server = models.ForeignKey(Server, verbose_name=_(u'Server'))
    ups = models.IntegerField(blank=False, help_text=_('Connected UPS'),
        choices=UPS_CHOICES, default=0)
