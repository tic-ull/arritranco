from django.db import models
from monitoring.nagios.models import NagiosOpts
from hardware.models import UnrackableNetworkedDevice


class SecurityDevice(UnrackableNetworkedDevice):
    # TODO
    def __unicode__(self):
        return u"%s, %s, %s" % (self.name, self.type.name, self.type.model.name)

    def model_name(self):
        return u"%s" % self.model.name

    def type_name(self):
        return u"%s" % self.model.type.name


class NagiosSecurityDeviceCheckOpts(NagiosOpts):
    securitydevice = models.ForeignKey(SecurityDevice)