from django.db import models
from monitoring.nagios.models import NagiosCheck
from hardware.models import UnrackableNetworkedDevice


class SecurityDevice(UnrackableNetworkedDevice):
    # TODO
    def __unicode__(self):
        return u"%s, %s, %s" % (self.name, self.type.name, self.type.model.name)

    def model_name(self):
        return u"%s" % self.model.name

    def type_name(self):
        return u"%s" % self.model.type.name


class NagiosSecurityDeviceCheckDefaults(models.Model):
    nagioscheck = models.ForeignKey(NagiosCheck)
    options = models.CharField(max_length=400)
    model = models.ForeignKey(SecurityDevice)