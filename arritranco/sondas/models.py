from django.db import models
from monitoring.nagios.models import NagiosOpts
from hardware.models import UserDevice
from inventory.models import Machine


class NagiosNrpeCheckOpts(NagiosOpts):
    service = models.ForeignKey("nagios.Service")
    sonda = models.ManyToManyField("Sonda")

    def __unicode__(self):
        return u"%s on %s by %s" % (self.check.name, self.service.name, self.sonda.name)

    def sonda_name(self):
        return str(self.sonda.name)

    def service_name(self):
        return str(self.service.name)

    def check_name(self):
        return str(self.check.name)


class Sonda(Machine):
    name = models.CharField(max_length=200, unique=True)
    userdevice = models.ForeignKey(UserDevice)
    ssh = models.BooleanField(default=False)
    dir_checks = models.CharField(default="/usr/lib/nagios/plugins", max_length=500, verbose_name="Directorio de plugings nagios")
    servidor_nagios = models.CharField(default="193.145.118.253", max_length=400)
    nrpe_service_name = models.CharField(default="nagios-nrpe-server", max_length=400)
    script_inicio = models.TextField(blank=True)
    script_end = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class SondaTask(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class SondaTasksLog(models.Model):
    sonda = models.ForeignKey(Sonda)
    task = models.ForeignKey(SondaTask)

    def __unicode__(self):
        return self.task.name + " " + self.sonda.name


class SondaTaskStatus(models.Model):
    STATUS_CHOICES = (
        (0, 'Correct'),
        (1, 'Know fail'),
        (2, 'Unknow fail'),
        (-1, 'Relaunched'),
    )
    tasklog = models.ForeignKey(SondaTasksLog)
    status = models.IntegerField(choices=STATUS_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.tasklog.task.name + str(self.status) + " " + str(self.timestamp)