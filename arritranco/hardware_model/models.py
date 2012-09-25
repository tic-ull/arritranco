from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

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
    
    def get_render_height(self):
        return settings.PX_FOR_UNITS * self.units
