from django.db import models
from location.models import Place, Building
from django.utils.translation import ugettext_lazy as _

SWITCH_LEVEL = (
    (10, _(u'Access')),
    (20, _(u'CPD')),
    (30, _(u'Distribution')),
    (40, _(u'Core')),
)

HD_CONN = (
    (0, 'SCSI'),
    (1, 'SATA'),
    (2, 'PATA'),
    (3, 'SAS'),
)

class HwType(models.Model):
    """This tool is intended to be used to store differents classes of hardware such as
    switches, servers, racks, workstations, displays, etc. Therefore we need a way to
    filter them"""
    name = models.CharField(max_length=255, help_text = _(u'Hardware Type Name'))
    slug = models.SlugField()

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name', ]

class Manufacturer(models.Model):
    """This class is for inventory of manufacturer we have"""
    name = models.CharField(max_length=255, help_text = _(u'Manufacturer Name'))
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        
class HwModel(models.Model):
    type = models.ForeignKey(HwType, help_text = _(u'Hardware Type'))
    manufacturer = models.ForeignKey(Manufacturer, help_text=_(u'Hardware Manufacturer'))
    name = models.CharField(max_length = 255, help_text = _(u'Name'))
    slug = models.SlugField()
    
    def __unicode__(self):
        return u"%s -- %s (%s)" % (self.manufacturer, self.name, self.type)
    
class RackableModel(HwModel):
    units = models.IntegerField()

class NetworkBaseModel(RackableModel):
    recommended_version = models.CharField(max_length = 255)
    ports = models.PositiveIntegerField(_(u'Default port number'))
    template = models.TextField()
    oid = models.CharField(max_length = 255,
            help_text = _(u'The string returned by this kind of hw when snmp queried about model')
            )

class HwBase(models.Model):
    """This class is the base for all other hardware classes. It includes
    only those common attributes for all hardware classes such as serial
    numbers. Any particular attribute goes in the closer model"""
    model = models.ForeignKey(HwModel, help_text = _('Hawrdware Model'))
    serial_number = models.CharField(max_length = 255, help_text = _(u'Hardware Serial Number'))

class Rack(HwBase):
    """This represent a RACK. It's possible interesting to include info for PDUs"""
    units_number = models.IntegerField()
    place = models.ForeignKey(Place)
    name = models.CharField(max_length = 255)
    slug = models.SlugField()

class RackPlace(models.Model):
    """This is for place in rack""" 
    rack = models.ForeignKey(Rack)
    base_unit = models.IntegerField()
    
class Rackable(HwBase, RackPlace):
    warranty_expires = models.DateField(blank=True, null=True)
    buy_date = models.DateField(blank=True, null=True)
    
class Unrackable(HwBase):
    building = models.ForeignKey(Building)

class UserDevice(Unrackable):
    name = models.CharField(max_length = 255)
    wall_socket = models.CharField(max_length = 255)
    port = models.ForeignKey("NetworkPort")
    place_in_building = models.TextField()
    comments = models.TextField()
    
class Phone(UserDevice):
    extension = models.CharField(max_length = 4)
    
class Server(Rackable):
    memory = models.DecimalField('GB RAM', max_digits=15, decimal_places=3, blank=True, null=True)
    processor_type = models.ForeignKey("ProcessorType", blank=True, null=True)
    processor_clock = models.DecimalField(_(u"Ghz"), max_digits=15, decimal_places=3, blank=True, null=True)
    processor_number = models.IntegerField(_(u'Number of processors'), help_text=_('Multi CPU servers has the same CPU type'))
    
class Chasis(Rackable):
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
    units = models.IntegerField()
    slots = models.IntegerField()
    
class BladeServer(Server):
    slots_number = models.CommaSeparatedIntegerField(max_length = 50, help_text=_(u'Slots used by this server'))
    chasis = models.ForeignKey(Chasis)
    
class HardDisk(models.Model):
    """
        Disco duro
    """
    server = models.ForeignKey(Server)
    size = models.DecimalField(_(u"GB"), max_digits=15, decimal_places=3, blank=True, null=True)
    conn = models.IntegerField(_(u"Tipo"), choices=HD_CONN, blank=True, null=True)

    def __unicode__(self):
        return u'%s Gb %s' % (self.size, self.get_conn_display())
    
class ProcessorType(models.Model):
    """
        Type of processor
    """
    manufacturer = models.ForeignKey(Manufacturer) 
    model = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s %s' % (self.manufacturer, self.modelo)

    class Meta:
        ordering = ['manufacturer', 'model']
        
class Switch(Rackable):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    ports = models.PositiveIntegerField()
    level = models.IntegerField(choices = SWITCH_LEVEL)
    model = models.ForeignKey(NetworkBaseModel)
    
class NetworkPort(models.Model):
    hw = models.ForeignKey(HwBase)
    name = models.CharField(max_length = 255)
    uplink = models.BooleanField(default = False)
    
class MACsHistory(models.Model):
    port = models.ManyToManyField(NetworkPort)
    captured = models.DateTimeField()
    mac = models.CharField(max_length=12) 

