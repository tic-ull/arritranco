# coding: utf-8

from django.db import models
from location.models import Room
from django.utils.translation import ugettext_lazy as _
from hardware_model.models import HwModel, Manufacturer
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import logging
logger = logging.getLogger(__name__)

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
    warranty_expires = models.DateField(blank=True, null=True)
    buy_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['model', 'serial_number']

    def __unicode__(self):
        return u"%s" % self.model.name

    def get_manufacturer_product_url(self):
        return self.model.manufacturer.get_product_url(self.serial_number)

class Rack(models.Model):
    """This represent a rack. It's possible interesting to include info for PDUs"""
    units_number = models.IntegerField()
    room = models.ForeignKey(Room)
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
    
    class Meta:
        verbose_name = _('Rack')
        verbose_name_plural = _('Racks')

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.room.name)    

    def get_render_height(self):
        return settings.PX_FOR_UNITS * self.units_number

class RackPlace(models.Model):
    """A place in a rack. This model is not intented to be used directly but as a
    base class for other models"""
    rack = models.ForeignKey(Rack)
    base_unit = models.IntegerField(help_text=_('The lowest U used by a rackable hardware'))
    # The total number of units used actually depends on the hardware

    class Meta:
        abstract = True

    def get_render_offset(self):
        if self.base_unit > 0:
            return settings.PX_FOR_UNITS * (self.base_unit - 1)
        else:
            return 0
    
class Unrackable(HwBase):
    """It's a non rackable hardware. It must be in a room"""
    room = models.ForeignKey(Room)
    
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
    
class Server(HwBase):
    """A generic server"""
    memory = models.DecimalField(max_digits = 15, decimal_places = 3, blank = True, null = True, help_text =_('Installed memory in GB'))
    management_ip = models.IPAddressField(help_text = _(u'Management or DRAC/iLO IP address'), blank = True, null = True)
    processor_type = models.ForeignKey("ProcessorType", blank = True, null=True)
    processor_clock = models.DecimalField(_(u"GHz"), max_digits = 15, decimal_places = 3, blank = True, null = True)
    # Multi CPU servers has the same CPU type
    processor_number = models.IntegerField(_(u'Number of processors'), help_text = _('Processors number'), default = 1)
    
    class Meta:
        verbose_name = _('Server')
        verbose_name_plural = _('Servers')

    def __unicode__(self):
        return u"%s (%s)" % (self.model, self.serial_number)

    def get_running_machine(self):
        try:
            return self.physicalmachine_set.get(up = True)
        except ObjectDoesNotExist:
            return None


class Chassis(HwBase, RackPlace):
    """A chassis is a hardware where we can plug servers, network cards, etc.
    Some samples: blade enclosures, modular switches, etc."""
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
    slots = models.IntegerField(help_text = _(u'Number of available slots'))

    class Meta:
        verbose_name = _('Chassis')
        verbose_name_plural = _('Chassis')

    def __unicode__(self):
        return u"Chasis (%s)" % (self.name)    
    
class BladeServer(Server):
    """A server to be plugged in a chassis"""
    slot_number = models.CommaSeparatedIntegerField(max_length = 50, help_text=_(u'Slots number used by this server'))
    chassis = models.ForeignKey(Chassis)

    class Meta:
        ordering = ['slot_number']
        verbose_name = _('Blade server')
        verbose_name_plural = _('Blade servers')


class RackServer(Server, RackPlace):
    """A rackable server"""

    class Meta:
        verbose_name = _('Rack server')
        verbose_name_plural = _('Rack servers')


class HardDisk(models.Model):
    """A hard disk"""
    server = models.ForeignKey(Server)
    size = models.DecimalField(_(u"GB"), max_digits=15, decimal_places=3, blank=True, null=True)
    conn = models.IntegerField(_(u"Type"), choices=HD_CONN, blank=True, null=True)

    class Meta:
        verbose_name = _('Hard disk')
        verbose_name_plural = _('Hard disks')

    def __unicode__(self):
        return u'%s Gb %s' % (self.size, self.get_conn_display())
    
class ProcessorType(models.Model):
    """
        Type of processor
    """
    manufacturer = models.ForeignKey(Manufacturer) 
    model = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s %s' % (self.manufacturer, self.model)

    class Meta:
        ordering = ['manufacturer', 'model']

