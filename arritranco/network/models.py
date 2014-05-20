'''
Created on 13/05/2011

@author: Agustin
'''
import IPy
from django.db import models
from location.models import Building
from hardware.models import RackPlace, NetworkedDevice
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from hardware.managementutils import sftpGet
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

SWITCH_LEVEL = (
    (10, _(u'Access')),
    (20, _(u'CPD')),
    (30, _(u'Distribution')),
    (40, _(u'Core')),
)

BACKUP_METHOD_NULL = 0
BACKUP_METHOD_SFTP = 1

SWITCH_BACKUP_METHOD = (
    (BACKUP_METHOD_NULL, _(u'No backup/Manual')),
    (BACKUP_METHOD_SFTP, _(u'SFTP')),
)

SWITCH_LEVEL_SNMP = {
    10: settings.SWITCH_LEVEL_SNMP_COMMUNITY_1,
    20: '--',
    30: '--',
    40: '--',
}

SWITCH_LEVEL_BACKUP_INFO = {
    10: (BACKUP_METHOD_SFTP, settings.BACKUP_METHOD_SFTP_USER, settings.BACKUP_METHOD_SFTP_PASSWORD),
    20: (BACKUP_METHOD_NULL, '', ''),
    30: (BACKUP_METHOD_NULL, '', ''),
    40: (BACKUP_METHOD_NULL, '', ''),
}

#class NetworkBaseModel(RackableModel):
#    recommended_version = models.CharField(max_length = 255)
#    ports = models.PositiveIntegerField(_(u'Default port number for this model'))
#    backupmethod = models.IntegerField(choices = SWITCH_BACKUP_METHOD)
#    backupusername = models.CharField(_(u'Backup username'), max_length = 255,
#            help_text = _(u'Backup username (credentials used in the backup process)')
#            )
#    backuppassword = models.CharField(_(u'Backup password'), max_length = 255,
#            help_text = _(u'Backup password (credentials used in the backup process)')
#            )
#    backupconfigfile = models.CharField(_(u'Backup configuration file'), max_length = 255,
#            help_text = _(u'Configuration file to backup ("path/file")')
#            )
#    template = models.TextField()
#    oid = models.CharField(max_length = 255,
#            help_text = _(u'The string returned by this kind of hw when snmp queried about model')
#            )


def ip_to_int(ip):
    """ Uses IPy to convert string ip to integer """
    return IPy.IP(ip).ip


def int_to_ip(num_ip):
    """ Uses IPy to convert integer ip to string """
    return IPy.IP(num_ip).strNormal()


def clean_netip(value):
    """ Control the string format and that the valule provided is valid IP addr using IPy module """
    try:
        ip = IPy.IP(value)
    except ValueError:
        raise ValidationError, _(u'You must provide a valid NETWORK IP address e.g.: 10.119.70.0/32')
    if not ('/' in value):
        raise ValidationError, _(u'You must use CIDR notation  \'xxx.xxx.xxx.xxx/xx\'')


def clean_ip(value):
    """ Check valid IPv4 addr """
    try:
        ip = IPy.IP(value)
    except ValueError:
        raise ValidationError, _(u'You must provide a valid IPv4 address e.g.: 10.119.70.0')


class Network(models.Model):
    """ Represents a network of the organization. """
    desc = models.CharField(help_text=_(u'Short description of the network context'), max_length=250)
    ip = models.CharField(help_text=_(u'Network ip address in CIDR notation e.g.: 10.119.70.0/24'), max_length=18,
                          validators=[clean_netip])
    first_ip = models.IPAddressField(help_text=_(u'First Host IP on network range'), editable=False)
    last_ip = models.IPAddressField(help_text=_(u'Last Host IP on network range'), editable=False)
    size = models.IntegerField(help_text=_(u'Number of Hosts in this network'), editable=False)

    def __unicode__(self):
        return u'Red %s (%s) - [%d Hosts]' % (self.ip, self.desc, self.size)

    def get_admin_url(self):
        return reverse('admin:network_network_change', args=(self.id,))

    def save(self, *args, **kwargs):
        """ Saving values we need to find network for a host. """
        self.last_ip = self._last_ip()
        self.first_ip = self._first_ip()
        self.last_ip_int = self._last_ip_int()
        self.first_ip_int = self._first_ip_int()
        self.size = IPy.IP(self.ip).len() - 2
        super(Network, self).save(*args, **kwargs)

    def netmask(self):
        """ Return str netmask for the network """
        return IPy.IP(self.ip).netmask().strNormal()

    def _first_ip(self):
        """ Returns str frist network host-ip """
        return IPy.IP(self.ip)[1].strNormal()

    def _last_ip(self):
        """ Returns str last network host-ip """
        return IPy.IP(self.ip)[-2].strNormal()

    def _first_ip_int(self):
        """ Returns integer frist network host-ip """
        return IPy.IP(self.ip)[1].int()

    def _last_ip_int(self):
        """ Returns integer last network host-ip """
        return IPy.IP(self.ip)[-2].int()

    def number_of_ips(self):
        return IP.objects.filter(network=self).count()


class IP(models.Model):
    addr = models.IPAddressField(help_text=_(u'IP v4 address'), validators=[clean_ip], unique=True)
    network = models.ForeignKey(Network, null=True, blank=True, editable=False, related_name="network_from_ip")

    def save(self, *args, **kwargs):
        """ Assigning the net to which this ip belongs to. """
        logger.debug("Calling IP Save method IP: %s", self.addr)
        nets = Network.objects.filter(first_ip__lte=self.addr, last_ip__gte=self.addr).order_by('size')
        if nets:
            logger.debug("There is net and assign: %s" % nets[0])
            self.network = nets[0]
            logger.debug("Result of asignation is: %s" % self.network)
        super(IP, self).save(*args, **kwargs)
        logger.debug("Saved IP: %d - %s" % (self.id, self))

    def network_addr(self):
        if self.network is None:
            return "No Network"
        else:
            return self.network.ip

    def __unicode__(self):
        return self.addr


class ManagementInfo(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        u'Descriptive name of the management info (I.e. "Procurve switch, basic credentials"'))
    defaultports = models.PositiveIntegerField(_(u'Default number of ports for this type of device'))
    backupmethod = models.IntegerField(choices=SWITCH_BACKUP_METHOD)
    backupusername = models.CharField(_(u'Backup username'), max_length=255,
                                      help_text=_(u'Backup username (credentials used in the backup process)')
    )
    backuppassword = models.CharField(_(u'Backup password'), max_length=255,
                                      help_text=_(u'Backup password (credentials used in the backup process)')
    )
    backupconfigfile = models.CharField(_(u'Backup configuration file'), max_length=255,
                                        help_text=_(u'Configuration file to backup ("path/file")')
    )
    recommended_version = models.CharField(max_length=255)
    configtemplate = models.TextField(_(u'Configuration template'))
    oid = models.CharField(max_length=255,
                           help_text=_(u'The string returned by this kind of hw when snmp queried about model')
    )

    def __unicode__(self):
        return u'%s' % self.name


class Switch(RackPlace, NetworkedDevice):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    ports = models.PositiveIntegerField()
    level = models.IntegerField(choices=SWITCH_LEVEL)
    managementinfo = models.ForeignKey(ManagementInfo)

    def __unicode__(self):
        return u'%s' % self.name

    #Backups switch configuration to the specified file
    #Returns
    #  False, "" : if no backup method defined for this switch
    #  True, None : If backup succeeded
    #  True, ErrorDescription : If backup failed
    def backup_config_to_file(self, destinationfile):
        mgt = self.managementinfo
        if mgt.backupmethod == BACKUP_METHOD_SFTP:
            errorDesc = sftpGet(hostname=self.main_ip, username=mgt.backupusername, password=mgt.backuppassword, \
                                sourcefile=mgt.backupconfigfile, destfile=destinationfile)
            return True, errorDesc
        return False, None


class RoutingZone(models.Model):
    """
        A model to represent a zone or group of buildings with common routing characteristics
    """
    prefix = models.CharField(max_length=6)
    name = models.CharField(max_length=255)
    bluevlan_prefix = models.IntegerField()
    public_nets = models.CharField(max_length=255,
                                   help_text=_(u"A list of public networks"))
    cajacanarias_nets = models.CharField(max_length=255,
                                         help_text=_(u"A list of CajaCanarias networks"))
    slug = models.SlugField()

    def __unicode__(self):
        return u'[%04d] %s - %s' % (int(self.bluevlan_prefix), self.prefix, self.name)


class NetworkedBuilding(Building):
    """
        A model to represent a Building with networking (with a routing zone)
    """
    routingzone = models.ForeignKey(RoutingZone)




