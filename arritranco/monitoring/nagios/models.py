from django.db.models.signals import post_save
from django.conf import settings
from scheduler.models import TaskStatus
from nsca import NSCA
from inventory.models import Machine
from monitoring.models import Responsible
from django.db import models
from django.utils.translation import ugettext_lazy as _

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

HUMAN_TO_NAGIOS = {
    'Ok': NAGIOS_OK,
    'ok': NAGIOS_OK,
    'bien': NAGIOS_OK,
    'yes': NAGIOS_OK,
    'Warning': NAGIOS_WARNING,
    'Critical': NAGIOS_CRITICAL,
    'Unknown': NAGIOS_UNKNOWN,
}

class NagiosCheck(models.Model):
    """ This represent a nagios check """
    name = models.CharField(max_length = 255)
    default = models.BooleanField(help_text="Say if this check is a default check")
    default_params = models.TextField(help_text="Default params for this check",blank = True, null = True)
    machines = models.ManyToManyField(Machine, through = 'NagiosCheckOpts', blank = True, null = True)
    slug = models.SlugField()
   
    def __unicode__(self):
        return u"%s" % self.name
    
    def all_machines(self):
        """ Returns all NagiosCheckOpts items which contains machine and options for the NagiosCheck """
        return self.nagioscheckopts_set.filter(machine__up = True)

class NagiosCheckOpts(models.Model):
    """ Check options for a NagiosCheck on a specific machine, oid's, ports etc.. """
    check = models.ForeignKey(NagiosCheck)
    machine = models.ForeignKey(Machine)
    options = models.CharField(max_length = 500, help_text="Parameter list to a nagios check", null = True, blank = True )
    contact_groups = models.ManyToManyField('NagiosContactGroup')
    
    def __unicode__(self):
        return u"%s on machine %s" % (self.check.name, self.machine.fqdn)
    def get_ngcontact_groups(self):
        """ Returns the contactcroup comaseparated line for the nagios conf """
        return ", ".join([x.ngcontact for x in self.contact_groups.all()])

class NagiosContactGroup(Responsible):
    """ A nagios concatc group to recieve alerts """
    ngcontact = models.CharField(_(u"Group name"),max_length = 100)    
    def __unicode(self):
        return u"%s (%s)" % (self.name, self.ng_contact)

def propagate_status(sender, **kwargs):
    if not settings.PROPAGATE_STATUS_TO_NAGIOS:
        return
    if kwargs['raw']:
        return

    status = kwargs['instance']
    task = status.task_check.task
    if hasattr(task, 'backuptask'):
        nsca = NSCA()
        status_code = HUMAN_TO_NAGIOS[status.status]
        nsca.add_custom_status(task.backuptask.machine.fqdn, task.description, status_code, status.comment)
        nsca.send()

post_save.connect(propagate_status, sender=TaskStatus)

