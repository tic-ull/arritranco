from django.db import models

class Responsible(models.Model):
    """ This models group/responsible of a machine for notifications and stuff... """
    name = models.CharField(max_length=255, blank=False)
    
    def __unicode__(self):
        return u"%s" % self.name
