from django.db import models
from location.models import Place
from django.utils.translation import ugettext_lazy as _

SWITCH_TYPE = ((10, _(u'Access')),
               (20, _(u'CPD')),
               (30, _(u'Distribution')),
               )

class HwType(models.Model):
    """This tool is intended to be used to store differents classes of hardware such as
    switches, servers, racks, workstations, displays, etc. Therefore we need a way to
    filter them"""
    name = models.CharField(max_length=255, help_text = _(u'Hardware Type Name'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name', ]

class Manufacturer(models.Model):
    """This class is for inventory of manufacturer we have"""
    name = models.CharField(max_length=255, help_text = _(u'Manufacturer Name'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
        
class HwModel(models.Model):
    type = models.ForeignKey(HwType, help_text = _(u'Hardware Type'))
    manufacturer = models.ForeignKey(Manufacturer, help_text=_(u'Hardware Manufacturer'))
    name = models.CharField(max_length = 255, help_text = _(u'Name'))
    
    def __unicode__(self):
        return u"%s -- %s (%s)" % (self.manufacturer, self.name, self.type)

class HwBase(models.Model):
    """This class is the base for all other hardware class. It includes
    only those common attributes for all hardware clases such as serial
    numbers. Any particular attribute goes in the closer model"""
    model = models.ForeignKey(HwModel, help_text = _('Hawrdware Model'))
    serial_number = models.CharField(max_length = 255, help_text = _(u'Hardware Serial Number'))

class Rack(HwBase):
    """This represent a RACK. It's possible interesting to include info for PDUs"""
    units_number = models.IntegerField()
    place = models.ForeignKey(Place)
    name = models.CharField(max_length = 255)

class RackPlace(Place):
    """This is for place in rack""" 
    rack = models.ForeignKey(Rack)
    start_unit = models.IntegerField()
    end_unit = models.IntegerField()
    
class Rackable(HwBase, RackPlace):
    #rack_place = models.ForeignKey(RackPlace)
    warranty_expires = models.DateField(blank=True, null=True)
    buy_date = models.DateField(blank=True, null=True)
    
class PhysicalServer(Rackable):
    units = models.CommaSeparatedIntegerField(max_length=50, help_text=_(u'Units used by this server'))
    
class Chasis(Rackable):
    units = models.IntegerField()
    slots = models.IntegerField()
    
class BladeServer(PhysicalServer):
    slots_number = models.CommaSeparatedIntegerField(max_length = 50, help_text=_(u'Slots used by this server'))
    chasis = models.ForeignKey(Chasis)

class Switch(Rackable):
    ports = models.IntegerField()
    type = models.IntegerField(choices = SWITCH_TYPE)