from django.db import models
from location.models import Place
from django.utils.translation import gettext_lazy as _


class Manufacturer(models.Model):
    """This class is for inventory of manufacturer we have"""
    name = models.CharField(max_length=255)
    wikiName = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name', ]
    
class HwType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name', ]
        
class HwModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    type = models.ForeignKey(HwType)

class HwBase(models.Model):
    """This class is the base for all other hardware class. It includes
    only those common attributes for all hardware clases such as serial
    numbers. Any particular attribute goes in the closer model"""
    model = models.ForeignKey(HwModel)
    serial_number = models.CharField(max_length = 255)

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
    
class Rackable(HwBase):
    rack_place = models.ForeignKey(RackPlace)
    warranty_expires = models.DateField(blank=True, null=True)
    buy_date = models.DateField(blank=True, null=True)
    
class PhysicalServer(Rackable):
    units = models.IntegerField()

class Switch(Rackable):
    ports = models.IntegerField()
    