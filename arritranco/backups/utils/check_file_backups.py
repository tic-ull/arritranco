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

import logging
import logging.config
from logging.handlers import *

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

URLBASE = 'https://inventario.stic.ull.es/rest/backup/backupfilechecker/?checker=xxxx'
UPDATEURL = 'https://inventario.stic.ull.es/rest/backup/set_integrity_status'
UPDATE_STATUS_URL = 'https://inventario.stic.ull.es/rest/scheduler/taskstatus/'
FILE_INFO_URL = 'https://inventario.stic.ull.es/rest/backup/BackupFileInfo'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s check_file_backups[%(levelname)s] %(module)s %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        },
        'brief': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'syslog':{
            'level':'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address': '/dev/log',
            'facility': SysLogHandler.LOG_LOCAL2,
        },
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/check_file_backups.log',
            'formatter': 'verbose',
            'backupCount': 50,
            'maxBytes': 2 ** 20,
        },
    },
    'loggers': {
        '__main__': {
            'handlers':['log_file'],
            'level':'DEBUG',
            'propagate': True,
        },
    },
}

if sys.stdout.isatty():
    LOGGING['handlers']['console'] = {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout'
        }
    LOGGING['loggers']['__main__']['handlers'].append('console')

# We might want to use a different one, e.g. importlib

def resolve(s):
    """
    Resolve strings to objects using standard import and attribute
    syntax.
    """
    importer = __import__
    name = s.split('.')
    used = name.pop(0)
    try:
        found = importer(used)
        for frag in name:
            used += '.' + frag
            try:
                found = getattr(found, frag)
            except AttributeError:
                importer(used)
                found = getattr(found, frag)
        return found
    except ImportError:
        e, tb = sys.exc_info()[1:]
        v = ValueError('Cannot resolve %r: %s' % (s, e))
        v.__cause__, v.__traceback__ = e, tb
        raise v


formatters = {}
for f in LOGGING['formatters'].keys():
    formatters[f] = logging.Formatter(LOGGING['formatters'][f]['format'])

handlers = {}
for h in LOGGING['handlers'].keys():
    config = {}
    for k,v in LOGGING['handlers'][h].items():
        config[k] = v
    factory = resolve(config.pop('class'))
    formatter = config.pop('formatter')
    if formatter:
        config['format'] = formatters[LOGGING['handlers'][h]['formatter']]
    config.pop('level')
    config.pop('format')
    if 'stream' in config:
        stream = config.pop('stream')
        config['strm'] = resolve(stream.split('/')[-1])
    handlers[h] = factory(**config)
    handlers[h].setLevel(logging._levelNames[LOGGING['handlers'][h]['level']])
    handlers[h].setFormatter(formatters[LOGGING['handlers'][h]['formatter']])
for l in LOGGING['loggers'].keys():
    logger = logging.getLogger(l)
    for h in LOGGING['loggers'][l]['handlers']:
        logger.addHandler(handlers[h])

logger = logging.getLogger(__name__)

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


class FileBackupProduct(object):
    def __init__(self, fbp, directory, host, verbose = False):
        self.host = host
        self.start_seq = fbp['start_seq']
        self.end_seq = fbp['end_seq']
        self.pattern = fbp['pattern'].replace('__FQDN__', self.host)
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

    def check(self, last_run, previous_run):
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
        logger.debug("Buscando: %s en %s" % (filename, self.directory))
        try:
            for f in os.listdir(self.directory):
                if fnmatch.fnmatch(f.lower(), filename.lower() + '*'):
                    msg = "  - Encontrado %s" % f
                    st = os.stat(os.path.join(self.directory, f))
                    if st[ST_MTIME] >= int(time.mktime(expected_time.timetuple())):
                        logger.debug("%s (En fecha y hora)" % msg)
                        files.append(f)
                    else:
                        logger.debug("%s (NO en fecha y hora)" % msg)
        except OSError, e:
            print e
            return None
        return files

    def check_sizes(self, filename, last_run, previous_run):
        def _is_compressed(filename):
            name, extension = os.path.splitext(filename)
            compressed = extension in ('.gz', '.zip', '.bz', '.bz2', '.rar')
            logger.debug("Fichero: %s" % filename)
            logger.debug("Extension: %s" % extension)
            logger.debug("Comprimido: %s" % compressed)
            return compressed

        logger.debug("Last run: %s" % last_run)
        last_run_files = self.search_file(last_run.strftime(filename), last_run)
        logger.debug("Previous run: %s" % previous_run)
        previous_run_files = self.search_file(previous_run.strftime(filename), previous_run)
        logger.debug("last run files: %s" % last_run_files)
        logger.debug("previous run files: %s" % previous_run_files)
        if not last_run_files:
            return (CRITICAL, 'No hay ultimo backup (%s)' % last_run)
        elif not previous_run_files:
            return (WARNING, "No hay backup anterior con el que comparar la copia del: %s [%s %s]" % (
                    last_run,
                    last_run_files[0],
                    sizeof_fmt(os.path.getsize(os.path.join(self.directory, last_run_files[0]))))
                )
        else:
            # We need manage the situation where we have more than one file in time.
            prev_file = os.path.join(self.directory, previous_run_files[0])
            last_file = os.path.join(self.directory, last_run_files[0])
            file_info = None
            if _is_compressed(last_file) != _is_compressed(prev_file):
                data = {
                    'file_name':os.path.basename(prev_file),
                    'directory':os.path.dirname(prev_file),
                    }
                file_info_url = FILE_INFO_URL + '?' +  urllib.urlencode(data)
                logger.debug("Descargando informacion del inventario para comparar los tamanyos originales")
                logger.debug("url: %s", file_info_url)
                try:
                    request = urllib2.Request(file_info_url, headers ={'Accept': 'application/json'})
                    res = urllib2.urlopen(request)
                    file_info = json.load(res)
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        logger.debug("No hay fichero en la base de datos")
                    else:
                        print e.read()
                        raise e
                except Exception, e:
                    print e
                    raise e
                if file_info is None:
                    return (WARNING, "No se pueden comparar los ficheros, uno esta comprimido y el otro no. (last:%s [%s] Vs previous:%s [%s])" % (
                                last_run_files[0],
                                sizeof_fmt(os.path.getsize(last_file)),
                                os.path.basename(prev_file),
                                sizeof_fmt(os.path.getsize(prev_file))
                                )
                            )
                else:
                    logger.debug("Informacion obtenida del inventario:")
                    for k,v in file_info.items():
                        logger.debug("   - %s: %s" % (k, v))
                size_min = self.variable_percentage / 100 * file_info['original_file_size']
                size_max = (1 + self.variable_percentage / 100) * file_info['original_file_size']
            else:
                size_min = self.variable_percentage / 100 * os.path.getsize(prev_file)
                size_max = (1 + self.variable_percentage / 100) * os.path.getsize(prev_file)
            if file_info is None:
                logger.debug("Comparando los siguientes ficheros con el umbral %s%%" % self.variable_percentage)
                logger.debug("   - ultimo %s (%s)" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
                logger.debug("   - anterior %s (%s)" % (previous_run_files[0], sizeof_fmt(os.path.getsize(prev_file))))
            else:
                logger.debug("Comparando los siguientes ficheros con el umbral %s%%" % self.variable_percentage)
                logger.debug("   - ultimo %s (%s)" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
                logger.debug("   - anterior segun el inventario %s (%s)" % (file_info['original_file_name'], sizeof_fmt(file_info['original_file_size'])))
            logger.debug("  Minimum aceptable size: %s" % size_min)
            logger.debug("  Maximum aceptable size: %s" % size_max)
            logger.debug("  Last backup size: %s" % os.path.getsize(last_file))
            if (os.path.getsize(last_file) >= size_min) and (os.path.getsize(last_file) <= size_max):
                logger.debug("  - OK")
                return (OK, "%s (%s)" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
            logger.debug("  - WARNING")
            return (WARNING, "Error: Los ficheros difieren mas de un %d%% (%s [%s] Vs %s [%s])" % (
                        self.variable_percentage,
                        last_run_files[0],
                        sizeof_fmt(os.path.getsize(last_file)),
                        previous_run_files[0],
                        sizeof_fmt(os.path.getsize(prev_file))
                    ))

class FileBackup(object):
    def __init__(self, backup, host, verbose = False):
        self.host = host
        self.id = int(backup['id'])
        self.last_run = datetime.datetime(*(time.strptime(backup['last_run'], '%Y-%m-%d %H:%M:%S')[0:6]))
        self.previous_run = datetime.datetime(*(time.strptime(backup['previous_run'], '%Y-%m-%d %H:%M:%S')[0:6]))
        self.directory = backup['directory']
        self.description = backup['description']
        self.products = []
        self.verbose = verbose
        for fbp in backup['files']:
            self.products.append(FileBackupProduct(fbp, backup['directory'], self.host, verbose))

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
            msg += " - %s\n" % s[1]
        return (global_status, msg)

    def get_dated_files(self, d):
        filepaths = []
        for fbp in self.products:
            for filename in fbp.get_dated_filenames(d):
                filepaths.append((filename, fbp.variable_percentage))
        return filepaths


if __name__ == "__main__":
    fqdn, dryrun = parseOpts()

    logger.setLevel(logging.INFO)
    if verbose:
        logger.setLevel(logging.DEBUG)

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
        logger.debug("---------------- Host: %s ---------------" % host)
        logger.debug("%s" % filesToCheck[host])
        logger.info("Checking host %s", host)
        for bckp in filesToCheck[host]:
            fbp = FileBackup(bckp, host, verbose)
            logger.info(" - Task %s", fbp.description)
            out = fbp.check_products()
            data = {
                'task':fbp.id,
                'task_time':fbp.last_run,
                'status':STATE_TO_HUMAN[out[0]],
                'comment':out[1]
            }
            logger.info("   * Status information: %s (%s)", data['status'], data['comment'].replace('\n', ''))
            if not dryrun:
                try:
                    logger.info("    * Sending status to inventory ...")
                    request = urllib2.Request(UPDATE_STATUS_URL, urllib.urlencode(data), {'Accept': 'application/json'})
                    res = urllib2.urlopen(request)
                except Exception, e:
                    logger.critical('Error sending status to inventory: %s', e)
                    raise e

                logger.info('      * Ok: %s', res.read())
            elif verbose:
                if data['task_time'] > datetime.datetime.now():
                    logger.debug("ERROR!!!!!!: task_time cant be in the future")
                    sys.exit(0)
                logger.debug(u"notify inventory: %s" % data)
            if nagios:
                print "%s\t%s\t%s\t%s" % (host, fbp.description, out[0], out[1])
            elif (verbose or (out[0] != OK)):
                logger.debug("%s %s: %s %s" % (host, fbp.description, STATE_TO_HUMAN[out[0]], out[1]))

