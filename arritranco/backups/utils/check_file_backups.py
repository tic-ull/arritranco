#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import urllib2
import urllib
import simplejson as json
import datetime
import getopt
import getpass
import socket
import os.path
import fnmatch
import platform
import locale
import time
from stat import *


# Default options
verbose = False
nagios = False

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

STATE_TO_HUMAN = {
    OK:'Ok',
    WARNING:'Warning',
    CRITICAL:'Critical',
    UNKNOWN:'Unknown',
}

URLBASE = 'http://localhost:8000/rest/backup/backupfilechecker/?checker=cdpbackup.sis.ccti.ull.es'
UPDATEURL = 'https://localhost:8000/rest/backup/set_integrity_status'
UPDATE_STATUS_URL = 'http://localhost:8000/rest/scheduler/taskstatus/'

def usage():
    """
        Prints help
    """
    print """
Usage: check_file_backups.py [options]

 -v  Verbose.
 -n  Nagios mode.
 -d  Dry run, do not update arritranco information
 -h  Print this help message
"""

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def parseOpts():
    """
        Parse command line options
    """
    global verbose, nagios
    fqdn = None
    dryrun = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vnhH:d")
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(1)
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o == "-n":
            nagios = True
        elif o == "-H":
            fqdn = a
        elif o == "-d":
            dryrun = True
        elif o == "-h":
            usage()
            sys.exit(0)
    return (fqdn, dryrun)


def update_inventory(id, status):
    global verbose

    try:
        res = urllib2.urlopen(UPDATEURL + "/%s/%s" % (id, status))
        if verbose:
            verde("       - Notificado el invenario correctamente.")
    except Exception, e:
        print e
        raise e

class FileBackupProduct(object):
    def __init__(self, fbp, directory, verbose = False):
        self.start_seq = fbp['start_seq']
        self.end_seq = fbp['end_seq']
        self.pattern = fbp['pattern']
        self.variable_percentage = float(fbp['variable_percentage'])
        self.directory = directory
        self.verbose = verbose

    def get_dated_filenames(self, run):
        filenames = []
        if self.start_seq:
            for chunk in range(self.start_seq, self.end_seq):
                filenames.append(self.pattern.replace('#', str(chunk)))
        else:
            filenames.append(self.pattern)
        return [run.strftime(f) for f in filenames]

    def check(self, previous_run, last_run):
        status= []
        if self.start_seq:
            for chunk in range(self.start_seq, self.end_seq + 1):
                filename = str(self.pattern.replace('#', str(chunk)))
                status.append(self.check_sizes(filename, last_run, previous_run))
        else:
            status.append(self.check_sizes(str(self.pattern), last_run, previous_run))
        return status

    def search_file(self, filename, expected_time):
        files = []
        if self.verbose:
            print "Buscando: %s en %s" % (filename, self.directory)
        try:
            for f in os.listdir(self.directory):
                if fnmatch.fnmatch(f.lower(), filename.lower() + '*'):
                    if self.verbose:
                        print "  - Encontrado %s" % f,
                    st = os.stat(os.path.join(self.directory, f))
                    if st[ST_MTIME] >= int(expected_time.strftime('%s')):
                        if self.verbose:
                            print "(En fecha y hora)"
                        files.append(f)
                    elif self.verbose:
                        print "(NO en fecha y hora)"
        except OSError, e:
            print e
            return None
        return files

    def check_sizes(self, filename, last_run, previous_run):
        last_run_files = self.search_file(last_run.strftime(filename), last_run)
        previous_run_files = self.search_file(previous_run.strftime(filename), previous_run)
        if self.verbose:
            print "last run files: %s" % last_run_files
            print "previous run files: %s" % previous_run_files
        if not last_run_files:
            return (CRITICAL, 'No hay ultimo backup')
        elif not previous_run_files:
            return (WARNING, "No hay backup anterior con el que comparar")
        else:
            # We need manage the situation where we have more than one file in time.
            prev_file = os.path.join(self.directory, previous_run_files[0])
            last_file = os.path.join(self.directory, last_run_files[0])
            if self.verbose:
                print "Comparando los siguientes ficheros con el umbral %s%%" % self.variable_percentage
                print "   - ultimo %s (%s)" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file)))
                print "   - anterior %s (%s)" % (previous_run_files[0], sizeof_fmt(os.path.getsize(prev_file)))
            size_min = self.variable_percentage / 100 * os.path.getsize(prev_file)
            size_max = (1 + self.variable_percentage / 100) * os.path.getsize(prev_file)
            if (os.path.getsize(last_file) >= size_min) or (os.path.getsize(last_file) <= size_max):
                if self.verbose:
                    print "  - OK"
                return (OK, "%s (%s)" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
            if self.verbose:
                print "  - WARNING"
            return (WARNING, "Error: Los ficheros difieren mas de un %d%%" % self.variable_percentage)

class FileBackup(object):
    def __init__(self, backup, verbose = False):
        self.id = int(backup['id'])
        self.last_run = datetime.datetime(*(time.strptime(backup['last_run'], '%Y-%m-%d %H:%M:%S')[0:6]))
        self.previous_run = datetime.datetime(*(time.strptime(backup['previous_run'], '%Y-%m-%d %H:%M:%S')[0:6]))
        #self.last_run = datetime.datetime.strptime(backup['last_run'], '%Y-%m-%d %H:%M:%S')
        #self.previous_run = datetime.datetime.strptime(backup['previous_run'], '%Y-%m-%d %H:%M:%S')
        self.directory = backup['directory']
        self.description = backup['description']
        self.products = []
        self.verbose = verbose
        for fbp in backup['files']:
            self.products.append(FileBackupProduct(fbp, backup['directory'], verbose))

    def check_products(self):
        status = []
        global_status = OK
        msg = ''
        for fbp in self.products:
            status += fbp.check(self.last_run, self.previous_run)
        for s in status:
            if s[0] == CRITICAL:
                global_status = s[0]
            elif s[0] == WARNING and global_status == OK:
                global_status = s[0]
            msg += " - %s" % s[1]
        return (global_status, msg)

    def get_dated_files(self, d):
        filepaths = []
        for fbp in self.products:
            for filename in fbp.get_dated_filenames(d):
                filepaths.append((filename, fbp.variable_percentage))
        return filepaths


if __name__ == "__main__":
    fqdn, dryrun = parseOpts()

    try:
        request = urllib2.Request(URLBASE, None, {'Accept': 'application/json'})
        res = urllib2.urlopen(request)
    except Exception, e:
        print e
        raise e

    filesToCheck = json.load(res)
    for host in filesToCheck.keys():
        if fqdn is not None and host != fqdn:
            continue
        if verbose:
            print "---------------- Host: %s ---------------" % host
        for bckp in filesToCheck[host]:
            fbp = FileBackup(bckp, verbose)
            if verbose:
                print "Tarea %s" % fbp.description
            out = fbp.check_products()
            data = {
                'task':fbp.id,
                'task_time':fbp.last_run,
                'status':STATE_TO_HUMAN[out[0]],
                'description':out[1]
            }
            if not dryrun:
                try:
                    request = urllib2.Request(UPDATE_STATUS_URL, urllib.urlencode(data), {'Accept': 'application/json'})
                    res = urllib2.urlopen(request)
                except Exception, e:
                    print e
                    raise e
            if nagios:
                print "%s\t%s\t%s\t%s" % (host, fbp.description, out[0], out[1])
            elif (verbose or (out[0] != OK)):
                print "%s: %s %s" % (fbp.description, STATE_TO_HUMAN[out[0]], out[1])

