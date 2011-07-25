from django.db import models
from location.models import Room, Building
from django.utils.translation import ugettext_lazy as _
from hardware_model.models import HwModel, Manufacturer

HD_CONN = (
    (0, 'SCSI'),
    (1, 'SATA'),
    (2, 'PATA'),
    (3, 'SAS'),
)

class HwBase(models.Model):
    """This class is the base for all other hardware classes. It includes
    only those common attributes for all hardware classes such as serial
    numbers. Any particular attribute goes in the closer model"""
    model = models.ForeignKey(HwModel, help_text = _('Hardware Model'))
    serial_number = models.CharField(max_length = 255, help_text = _(u'Hardware Serial Number'))

class Rack(models.Model):
    """This represent a RACK. It's possible interesting to include info for PDUs"""
    units_number = models.IntegerField()
    room = models.ForeignKey(Room)
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
    
    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.room.name)    

class RackPlace(models.Model):
    """This is for place in rack"""
    rack = models.ForeignKey(Rack)
    base_unit = models.IntegerField()
    
class Rackable(HwBase, RackPlace):
    warranty_expires = models.DateField(blank=True, null=True)
    buy_date = models.DateField(blank=True, null=True)
    units = models.CommaSeparatedIntegerField(max_length=300, help_text = _(u'Units the server takes'))
    
class Unrackable(HwBase):
    building = models.ForeignKey(Building)
    
class NetworkedDevice(models.Model): 
    main_ip = models.IPAddressField(help_text = _(u'Management or main IP address'))
    
class NetworkPort(models.Model):
    hw = models.ForeignKey(HwBase)
    name = models.CharField(max_length = 255)
    uplink = models.BooleanField(default = False)    

class UserDevice(Unrackable, NetworkedDevice):
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
    
    def __unicode__(self):
        return u"%s (%s)" % (self.model, self.serial_number)    

class Chasis(Rackable):
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
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

