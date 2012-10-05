# -*- coding: utf-8 -*-
from django.conf import settings
import logging
import sys
import time
if sys.version_info < (2, 4):
    import popen2
else:
    import subprocess

logger = logging.getLogger(__name__)

def process(cmd, stdin="", ignore_error=False):
    if sys.version_info < (2, 4):
        p = popen2.Popen3(cmd, True)
        if stdin:
            p.tochild.write(stdin)
            p.tochild.flush()
            p.tochild.close()
        out = p.fromchild.read()
        err = p.childerr.read()
        returncode = p.wait()
    else:
        if stdin:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                p.stdin.write(stdin)
            except IOError, e:
                logger.error('Error writing "%s" to stdin while running %s: %s\n\n%s', stdin, cmd, e, p.stdout.read())
        else:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = p.communicate()
        returncode = p.returncode

    if returncode != 0 and not ignore_error:
        raise RuntimeWarning("Error code: %d\n%s" % (returncode, err))

    return (out, err)


class NSCA:
    NAGIOS_OK = 0
    NAGIOS_WARNING = 1
    NAGIOS_CRITICAL = 2
    NAGIOS_UNKNOWN = 2

    def __init__(self, timeout=300):
        self.timeout = timeout
        self.nagios_status = []

    def add_ok(self, host, service, message):
        self.nagios_status.append( (host, service, Nagios.NAGIOS_OK, message) )

    def add_warning(self, host, service, message):
        self.nagios_status.append( (host, service, Nagios.NAGIOS_WARNING, message) )

    def add_critical(self, host, service, message):
        self.nagios_status.append( (host, service, Nagios.NAGIOS_CRITICAL, message) )

    def add_custom_status(self, host, service, status, message):
        if int(status) not in [NSCA.NAGIOS_OK, NSCA.NAGIOS_WARNING, NSCA.NAGIOS_CRITICAL, NSCA.NAGIOS_UNKNOWN]:
            raise RuntimeError('%s is not a valid nagios status')
        self.nagios_status.append( (host, service, int(status), message) )

    def get_nagios_status(self):
        out = ""
        for host, service, status, message in self.nagios_status:
            result = u'%s\t%s\t%s\t%s\n' % (host, service, status, message.replace('\n', ' '))
            out += result
        return out.encode('utf-8')

    def send(self, debug=False):
        if debug:
            print "Command: ", settings.SEND_NSCA_BIN
            print "NSCA daemon: ", settings.NSCA_DAEMON_HOSTNAME
            print "Timeout: ", self.timeout
            print "Config: ", settings.SEND_NSCA_CFG
            print "Status: ", self.get_nagios_status()
            return None
        else:
            cmd = [
                settings.SEND_NSCA_BIN,
                "-H", settings.NSCA_DAEMON_HOSTNAME,
                "-to", str(self.timeout),
                "-c", settings.SEND_NSCA_CFG
            ]
            return process(cmd, self.get_nagios_status(), ignore_error=False)
