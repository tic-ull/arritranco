from django.db import models

# Create your models here.

class Manufacturer(models.Model):
    """This class is for inventory of manufacturer we have"""
    name = models.CharField(max_length=255)
    wikiName = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name', ]

class Thing(models.Model):
    """This class is for inventory those things that cannot be considered hardware"""
    manufacturer = models.ForeignKey(Manufacturer, null = True, blank = True)
    name = models.CharField(max_length = 255)