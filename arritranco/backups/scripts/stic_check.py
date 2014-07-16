from __future__ import absolute_import

from celery import Celery
from django.conf import settings
import os,sys
import datetime
from django.template import Template, Context
import urllib2
import urllib
import simplejson as json
import datetime
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
import gzip
from stat import *
if platform.python_version_tuple() > (2, 5):
    import hashlib
else:
    import md5


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

logger = logging.getLogger(__name__)

class MD5File(file):
    def __init__(self, fname, mode='r'):
        if platform.python_version_tuple() > (2, 5):
            self.m = hashlib.md5()
        else:
            self.m = md5.new()
        file.__init__(self, fname, mode)

    def write(self, buff):
        self.m.update (buff)
        file.write(self, buff)

    def writelines(self, buff):
        file.writelines(self, buff)

    def hexdigest(self):
        return self.m.hexdigest()


def compress(id, filename):
    compressedfilename = filename + '.gz'
    if platform.python_version_tuple() > (2, 5):
        md5sum = hashlib.md5()
    else:
        md5sum = md5.new()
    logger.info(u"Abriendo para lectura: %s" % filename)
    try:
        f_in = open(filename, 'rb')
    except Exception, e:
        logger.info(e)
        return False
    logger.info(u"Abriendo para escritura: %s" % compressedfilename)
    _f_out = MD5File(compressedfilename, 'wb')
    f_out = gzip.GzipFile(fileobj=_f_out, compresslevel=9)
    logger.infoi(u"Comprimiendo y calculando md5: %s" % filename)

    while True:
        line = f_in.read(1024)
        md5sum.update (line)
        f_out.write (line)
        if len(line) == 0:
            break
    f_out.close()
    compressed_md5 = _f_out.hexdigest()
    _f_out.close ()
    f_in.close()
    os.unlink (filename) 
    logger.info(u"Fin de la compresion de: %s" % filename)
    original_md5 = md5sum.hexdigest()
    notify_compressed_file (id, compressedfilename, original_md5 = original_md5, compressed_md5 = compressed_md5)
    return md5sum

def notify_compressed_file (id, filename, original_md5 = None, compressed_md5 = None, url = None):
    try:
        filesize = os.stat(filename).st_size
        filedate = os.stat(filename).st_ctime
    except OSError, e:
        logger.info("OSError: ", e)
        return
    if compressed_md5 is None:
        if platform.python_version_tuple() > (2, 5):
            hash = hashlib.md5()
        else:
            hash = md5.new()
        f = open (filename, 'rb')
        while True:
            line = f.read(1024)
            hash.update (line)
            if len(line) == 0:
                break
        f.close ()
        compressed_md5 = hash.hexdigest ()
    data = {
        'directory': os.path.dirname(filename),
        'filedate': filedate,
        'filesize': filesize,
        'compressedfilename': os.path.basename (filename),
        'compressedmd5': compressed_md5,
    }
    if original_md5 is not None:
        data['originalmd5'] = original_md5
    if id:
        data['id'] = id
    query = urllib.urlencode(data)
    if url is None:
        url = settings.BACKUP_URLCOMPRESS + query
    else:
        url += query
    try:
        logger.info(u"Llamando: %s" % (url))
        res = urllib2.urlopen(url)
    except Exception, e:
        logger.info(e)
        raise e


def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def _is_compressed(filename):
    name, extension = os.path.splitext(filename)
    compressed = extension in ('.gz', '.zip', '.bz', '.bz2', '.rar', '.gzip')
    logger.info("Fichero: %s ( %s ) Comprimido: %s" % (filename, extension, compressed))
    return compressed

class FileBackupProduct_Checker(object):
    def __init__(self, fbp, directory, host):
        self.host = host
        self.start_seq = fbp['start_seq']
        self.end_seq = fbp['end_seq']
        self.pattern = fbp['pattern'].replace('__FQDN__', self.host)
        self.variable_percentage = float(fbp['variable_percentage'])
        self.directory = directory

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
        logger.info("Buscando: %s en %s" % (filename, self.directory))
        try:
            for f in os.listdir(self.directory):
                if fnmatch.fnmatch(f.lower(), filename.lower() + '*'):
                    msg = "  - Encontrado %s" % f
                    st = os.stat(os.path.join(self.directory, f))
                    if st[ST_MTIME] >= int(time.mktime(expected_time.timetuple())):
                        logger.info("%s (En fecha y hora)" % msg)
                        files.append(f)
                    else:
                        logger.info("%s (NO en fecha y hora)" % msg)
        except OSError, e:
            logger.info(e)
            return None
        return files

    def check_sizes(self, filename, last_run, previous_run):

        logger.info("--------- %s --------" % filename)
        last_run_files = self.search_file(last_run.strftime(filename), last_run)
        previous_run_files = self.search_file(previous_run.strftime(filename), previous_run)
        logger.info("Ultima ejecucion (%s): %s  ||| Anterior (%s): %s " % (last_run,last_run_files,previous_run,previous_run_files))
        if not last_run_files:
            return (CRITICAL, 'No hay backup [%s] (%s)' % (filename,last_run))
        elif not previous_run_files:
            return (WARNING, "No hay backup anterior con el que comparar la copia del: %s [%s %s]" % (
                    last_run,
                    last_run_files[0],
                    sizeof_fmt(os.path.getsize(os.path.join(self.directory, last_run_files[0]))))
                )
        else:
            prev_file = os.path.join(self.directory, previous_run_files[0])
            last_file = os.path.join(self.directory, last_run_files[0])
            file_info = None
            if _is_compressed(last_file) != _is_compressed(prev_file):
                # We need manage the situation where we have more than one file in time.
                data = {
                    'file_name':os.path.basename(prev_file),
                    'directory':os.path.dirname(prev_file),
                    'checker':'dbackup.stic.ull.es',
                    }
                file_info_url = settings.BACKUP_FILE_INFO_URL + '?' +  urllib.urlencode(data)
                logger.info("Descargando informacion del inventario: %s", file_info_url )
                try:
                    request = urllib2.Request(file_info_url, headers ={'Accept': 'application/json'})
                    res = urllib2.urlopen(request)
                    file_info = json.load(res)
                    size_min = file_info['original_file_size'] - self.variable_percentage / 100 * file_info['original_file_size']
                    size_max = (1 + self.variable_percentage / 100) * file_info['original_file_size']
                    old_size = sizeof_fmt(file_info['original_file_size'])
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        logger.info("No hay fichero en la base de datos")
                    else:
                        logger.info(e.read())
                        raise e
                except Exception, e:
                    logger.info(e)
                    raise e
            else:
                size_min = os.path.getsize(prev_file) - self.variable_percentage / 100 * os.path.getsize(prev_file)
                size_max = (1 + self.variable_percentage / 100) * os.path.getsize(prev_file)
                old_size = sizeof_fmt(os.path.getsize(prev_file))
            if file_info is None:
                logger.info("Comparando los siguientes ficheros con el umbral %s%% ( ultimo: %s [%s], anterior: %s [%s])" % (self.variable_percentage,last_run_files[0], sizeof_fmt(os.path.getsize(last_file)),previous_run_files[0], sizeof_fmt(os.path.getsize(prev_file))))
            else:
                logger.info("Comparando los siguientes ficheros con el umbral %s%% ( ultimo: %s [%s], anterior segun inventario: %s [%s])" % (self.variable_percentage, last_run_files[0], sizeof_fmt(os.path.getsize(last_file)),file_info['original_file_name'], sizeof_fmt(file_info['original_file_size'])))
            logger.info("  Ultimo backup: %s ( Min: %s, Max: %s)" % (os.path.getsize(last_file),size_min, size_max))
            if  (os.path.getsize(last_file) >= size_min) and (os.path.getsize(last_file) < 400 * 1024):
                logger.info("  FS < 400KB - OK")
                return (OK, "%s (%s) FS < 400KB" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
            if (self.variable_percentage == 0):
                logger.info("  FS not chequeado- OK")
                return (OK, "%s (%s) Omitiendo" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
            if (os.path.getsize(last_file) >= size_min) and (os.path.getsize(last_file) <= size_max):
                logger.info("  - OK")
                return (OK, "%s (%s)" % (last_run_files[0], sizeof_fmt(os.path.getsize(last_file))))
            logger.info("  - WARNING")
            return (WARNING, "Error: Los ficheros difieren mas de %d%% (%s [%s] Vs %s [%s])" % (
                        self.variable_percentage,
                        last_run_files[0],
                        sizeof_fmt(os.path.getsize(last_file)),
                        previous_run_files[0],
                        old_size,
                    ))

class FileBackup_Checker(object):
    def __init__(self, backup, host, directory):
        self.host = host
        self.id = int(backup['id'])
        self.last_run = datetime.datetime(*(time.strptime(backup['last_run'], '%Y-%m-%dT%H:%M:%S')[0:6]))
        self.previous_run = datetime.datetime(*(time.strptime(backup['previous_run'], '%Y-%m-%dT%H:%M:%S')[0:6]))
        self.directory = directory
        self.description = backup['description']
        self.products = []
        for fbp in backup['files']:
            self.products.append(FileBackupProduct_Checker(fbp, self.directory, self.host))

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


def compress_Checker(backup_id,filename):
    md5sum=None
    if not _is_compressed(filename):
        md5sum = compress (backup_id, filename)
        filename = filename + '.gz'
    notify_compressed_file (backup_id, filename, md5sum)

def deletefile_Checker(filename):
    try:
        if os.path.exists(filename):
            os.unlink(filename)
        else:
            logger.info("FALLO: error borrando fichero")
            failed.append(filename)
    except Exception, e:
         logger.info("\n!!!!!ERROR!!!!!: ", e)

    try:   # Se marca como borrado en inventario.
         data = urllib.urlencode([('deleted_files',filename)])
         res = urllib2.urlopen(settings.BACKUP_URLDELETE, data)
         response = json.load(res)
         logger.info (response)
         status = response[0][1]
    except urllib2.HTTPError,e :
         logger.info("No se ha podido borrar")
         logger.info(e)
         logger.info(e.read())
         status = False

def verifybackup_Checker(fqdn, id, directory):
    logger.setLevel(logging.INFO)
    try:
        url = settings.BACKUP_URLBASE + "&id=" + id
        request = urllib2.Request(url, None, {'Accept': 'application/json'})
        res = urllib2.urlopen(request)
    except Exception, e:
        logger.info(e)
        raise e

    filesToCheck = json.load(res)
    for host in filesToCheck.keys():
        if host == fqdn:
            logger.info(">>>>>> Checking  %s <<<<<<" , host)
            for bckp in filesToCheck[host]:
                 fbp = FileBackup_Checker(bckp, host, directory)
                 logger.info(" - Task HOST %s", fbp.description)
                 out = fbp.check_products()
                 data = {
                     'check_time': datetime.datetime.now(),
                     'status': STATE_TO_HUMAN[out[0]],
                     'comment': out[1]
                 }
                 logger.info("   * Estado: %s (%s)", data['status'], data['comment'].replace('\n', ''))
                 try:
                     url = settings.BACKUP_UPDATE_STATUS_URL % fbp.id
                     logger.info("    * Enviando el estado al inventario %s (%s)" % (url, data))
                     request = urllib2.Request(url, urllib.urlencode(data), {'Accept': 'application/json'})
                     res = urllib2.urlopen(request)
                 except Exception, e:
                     logger.critical('Error sending status to inventory: %s', e)
                     raise e

                 logger.info('      * Ok: %s', res.read())
#                 logger.info "%s\t%s\t%s\t%s" % (host, fbp.description, out[0], out[1])
                 logger.info("%s %s: %s %s" % (host, fbp.description, STATE_TO_HUMAN[out[0]], out[1]))
        else:
            logger.info("wrong filecheckid")

