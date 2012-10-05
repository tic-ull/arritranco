#! /usr/bin/python
# -*- coding: utf-8 -*-

import platform
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE
import datetime
import time
import calendar

import getpass
import os
import sys
import locale
import urllib2
import csv
import simplejson as json

class TSMBaseParser:
    def __init__(self):
        self.data = []
        self.error = []
        self.serverCommand = ''
        self.returnCode = ''

    def parse(self, line):
        print line

    def ANSParser(self, line):
        if line.startswith('ANS8000I'):
            self.serverCommand = line
        elif line.startswith('ANS8002I'):
            self.returnCode = line
        else:
            self.error.append(line)

class TSMQueryRequestParser(TSMBaseParser):
    """
    tsm: BACKUP-SAN_SERVER1>q req
    ANR8352I Requests outstanding:
    ANR8373I 015: Fill the bulk entry/exit port of library TS3310_0 with all LTO volumes to be processed within 55 minute(s); issue 'REPLY' along with the
    request ID when ready.
    """

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.requests = []

    def parse(self, line):
        line = line.strip()
        if line.startswith('ANS'):
            self.ANSParser(line)
        elif line.startswith('ANR8346I'):
            print "No requests are outstanding."
        elif line.startswith('ANR8306I'):
            self.requests.append(line.split(':')[0].split(' ')[1])
        elif line.startswith('ANR8373I'):
            self.requests.append(line.split(':')[0].split(' ')[1])

class TSMMountParser(TSMBaseParser):
    MAX_DRIVES_USED = 4

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.drivesBussy = 0

    def freeDrives(self):
        return self.drivesBussy < TSMMountParser.MAX_DRIVES_USED

    def parse(self, line):
        line = line.strip()
        if line.startswith('ANS'):
            self.ANSParser(line)
        elif line.startswith('ANR2034E'):
            self.drivesBussy = 0
        elif line.startswith('ANR8329I') or line.startswith('ANR8330I') or line.startswith('ANR8379I'):
            self.drivesBussy += 1

class TSMLibvolParser(TSMBaseParser):
    SKIP_PHASE = 0
    DATA_PHASE = 1

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.phase = TSMLibvolParser.SKIP_PHASE
        self.catridages = {}

    def parse(self, line):
        line = line.strip()
        if line.startswith('ANS'):
            self.ANSParser(line)
        if self.phase == TSMLibvolParser.SKIP_PHASE:
            if line.startswith('-----'):
                self.phase = TSMLibvolParser.DATA_PHASE
        elif line == '':
            self.phase = TSMLibvolParser.SKIP_PHASE
        else:
    # La línea debe tener esta pinta, los campos son de ancho fijo
    #Library Name     Volume Name     Status               Owner          Last Use      Home        Device Type                                                                                   Element     Type
    #------------     -----------     ----------------     ----------     ---------     -------     ------
    #L80              000062          Scratch                                           1,004       LTO

            library = line[0:12].strip()
            volumename = line[17:29].strip()
            status = line[33:50].strip()
            owner = line[54:65].strip()
            last_usage = line[69:79].strip()
            home = line[83:91].strip()
            device_type = line[95:103].strip()
            self.catridages["%s_%s" % (library, volumename)] = (volumename, status, owner, last_usage, home, device_type)

class TSMBackupTapeParser(TSMBaseParser):
    SKIP_PHASE = 0
    DATA_PHASE = 1

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.phase = TSMSelectParser.SKIP_PHASE

    def getLast(self, number):
        return self.data[-number:]

    def parse(self, line):
        line = line.strip()
        if line.startswith('ANS'):
            self.ANSParser(line)
        if self.phase == TSMSelectParser.SKIP_PHASE:
            if line.startswith('-----'):
                self.phase = TSMSelectParser.DATA_PHASE
        elif line == '':
            self.phase = TSMSelectParser.SKIP_PHASE
        else:
    # La línea debe tener esta pinta, los campos son de ancho fijo
    # 12/13/08   08:14:07      BACKUPFULL          1,026             0          1     LTO3CLASS        A00110
            date = line[0:19]
            tape = line[97:107]
            self.data.append("%s (%s)" % (tape, date))

class TSMActLogParser(TSMBaseParser):
    SKIP_PHASE = 0
    DATA_PHASE = 1
#   FILE = None

    def __init__(self):
        TSMBaseParser.__init__(self)
#        if not TSMActLogParser.FILE:
#            TSMActLogParser.FILE = open('/tmp/actlog.log', 'w')
        self.phase = TSMActLogParser.SKIP_PHASE
        self.data = []
        self.aux = { 'date':None, 'message':None}
        if platform.platform().startswith("Windows"):
            self.platform = "Windows"
        else:
            self.platform = "Linux"

    def reset(self):
        self.data = []

    def getLast(self, number):
        return self.data[-number:]

    def parse(self, line):
#        TSMActLogParser.FILE.write(line + '\n')
        if line.startswith('ANS'):
            self.ANSParser(line)
        if self.phase == TSMActLogParser.SKIP_PHASE:
            if line.startswith('-----'):
                self.phase = TSMActLogParser.DATA_PHASE
        elif self.phase == TSMActLogParser.DATA_PHASE:
            if line == '\n':
                self.phase = TSMActLogParser.SKIP_PHASE
                return
            #Date/Time                Message
            #--------------------     ----------------------------------------------------------
            #12/18/08   12:44:34      ANR8437E CHECKOUT LIBVOLUME for volume A00033 in library
            #                          TS3310_0 failed. (SESSION: 4518, PROCESS: 50)
            if line.startswith("        "):
                self.aux['message'] += ' ' + line.strip()
                return
            if self.aux['date']:
                self.data.append(dict(self.aux))
                #print "(%s) -> %s" % (len(self.data), self.aux)
                self.aux['date'] = None
            if self.platform == "Windows":
                self.aux['date'] = datetime.datetime.strptime(line[0:19], '%d.%m.%y   %H:%M:%S')
            else:
                self.aux['date'] = datetime.datetime.strptime(line[0:19], '%m/%d/%y   %H:%M:%S')
            self.aux['message'] = line[25:]
        else:
            print line

class TSMProcessParser(TSMBaseParser):
    SKIP_PHASE = 0
    DATA_PHASE = 1

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.phase = TSMProcessParser.SKIP_PHASE
        self.procesos = {}
        self.last_id = None

    def parse(self, line):
        if line.startswith('ANS'):
            self.ANSParser(line)
            if line.startswith('ANS8002I'):
                self.phase = TSMProcessParser.SKIP_PHASE
#                for id in self.procesos.keys():
#                    print "id: %s ->" % id, self.procesos[id]
                return

        if line.startswith('ANR0944E'):
            # ANR0944E QUERY PROCESS: No active processes found.
            pass
        if self.phase == TSMProcessParser.SKIP_PHASE:
            if line.startswith('-------'):
                self.phase = TSMProcessParser.DATA_PHASE
                return
        elif self.phase == TSMProcessParser.DATA_PHASE:
            # Campos de longitud fija ...
            #--------     --------------------     -------------------------------------------------
            #      48     Space Reclamation        Offsite Volume(s) (storage pool LTO3POOL_COPY),
            #                                       Moved Files: 23, Moved Bytes: 4,149,250,332,
            #                                       Unreadable Files: 0, Unreadable Bytes: 0.
            #                                       Current Physical File (bytes): 1,165,593,708
            #                                       Current input volume: A00079. Current output
            #                                       volume: A00068.
            if line.strip() == '':
                return
            if line.startswith("        "):
                self.procesos[self.last_id]['status'] += line.strip()
                return
            self.last_id = int(line[0:8].strip())
            description = line[8:32].strip()
            status = line[32:].strip()
            self.procesos[self.last_id] = {
                'description':description,
                'status':status}
        elif line == '':
            self.phase = TSMProcessParser.SKIP_PHASE
        else:
            print "linea: %s" % line

class TSMSelectParser(TSMBaseParser):
    SKIP_PHASE = 0
    DATA_PHASE = 1

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.phase = TSMSelectParser.SKIP_PHASE

    def parse(self, line):
        line = line.strip()
        if line.startswith('ANS'):
            self.ANSParser(line)
        if self.phase == TSMSelectParser.SKIP_PHASE:
            if line.startswith('-----'):
                self.phase = TSMSelectParser.DATA_PHASE
        elif line == '':
            self.phase = TSMSelectParser.SKIP_PHASE
        else:
            self.data.append(line)

class TSM_CSVSelectParser(TSMBaseParser):
    SKIP_PHASE = 0
    DATA_PHASE = 1

    def __init__(self):
        TSMBaseParser.__init__(self)
        self.phase = TSMSelectParser.SKIP_PHASE

    def parse(self, line):
        line = line.strip()
        if line.startswith('ANS'):
            self.ANSParser(line)
        if self.phase == TSMSelectParser.SKIP_PHASE:
            if self.serverCommand != '':
                self.phase = TSMSelectParser.DATA_PHASE
        elif line == '':
            self.phase = TSMSelectParser.SKIP_PHASE
        elif line.startswith('ANR'):
            self.phase = TSMSelectParser.SKIP_PHASE
        else:
            for row in csv.reader([line]):
                self.data.append(row)

class TSMClient:
    """
    Clase para interactuar con el cliente de línea de comandos de Tivoli Storage Manager
    """
    WINDOWS = False

    TSM_INVALID_PASSWORD=137
    TSM_UNEXPECTED_SQL=3

    def __init__(self, dsmcPath = None, log = None, username = 'admin', server = None):
        if dsmcPath is not None:
            self.dsmcPath = str(dsmcPath)
        self.log = log
        self.server = server
        self.username = username
        self.password = None
        if platform.platform().startswith("Windows"):
            self.loguea("Corriendo en Windows")
            TSMClient.WINDOWS = True
        else:
            self.loguea("Corriendo en Linux")

    def loguea(self, msg):
        if self.log is not None:
            self.log.addMSG(msg)

    def getDsmcPath(self):
        return self.dsmcPath

    def setDsmcPath(self, dsmcPath):
        self.dsmcPath = str(dsmcPath)

    def setUsername(self, username):
        self.username = str(username)

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        self.password = str(password)

    def passwordDialog(self):
        self.setPassword(getpass.getpass('Introduce el password para el TSM: '))
        return True

    def run_TSMcommand(self, command, parser = None):
        "-id=<usuario/> -password=<password/> <command/>"
        if self.password is None and not self.passwordDialog():
            print "Pon un password cenizo"
            return False
        if self.dsmcPath is None:
            self.loguea("No se donde está el ejecutable del dsmcadm")
            return False
        self.loguea("\n\n\t--------- Consultando TSM (%s) -------\n\n" % datetime.datetime.now().strftime("%d:%m:%Y %H:%M"))
        tsm_args = ' -id=%s -password=%s ' % (self.username, self.password)
        if self.server:
            tsm_args += '-server=%s ' % self.server
        tsm_args += command
        if TSMClient.WINDOWS:
            executable = "dsmadmc.exe"
            cmd = executable + tsm_args
        else:
            os.environ['LANG'] = 'C'
            os.environ['LD_LIBRARY_PATH'] = os.path.join(*(['/'] + self.dsmcPath.split('/')[:-3] + ['api', 'bin']))
            executable = "dsmadmc"
            cmd = self.dsmcPath + executable + tsm_args
        self.run_command(cmd, self.dsmcPath, executable, parser)
        return True

    def run_TSM_CSV_Command(self, command, parser = None):
        return self.run_TSMcommand(' -commadelimited ' + command, parser)

    def run_command(self, command, cwd, executable, parser = None):
        self.loguea(command)
        try:
            if TSMClient.WINDOWS:
                os.chdir(cwd)
            else:
                executable = os.path.join(cwd, executable)
                cwd = None
            process =  Popen(command.split(), executable=executable, stderr = STDOUT, stdout = PIPE, cwd = cwd)
            pipe = process.stdout
            while True:
                line = pipe.readline()
                if not line: break
                if TSMClient.WINDOWS:
                    line = unicode(line.decode('cp850'))
                #line = line.strip()
                self.loguea("%s" % line[:-1])
                if parser is not None:
                    parser(line)
                else:
                    print line
        except OSError, e:
            print e
            sys.exit(0)
        process.wait()
        if process.returncode is None:
            print "El comando no ha terminado correctamente."
        elif process.returncode == TSMClient.TSM_INVALID_PASSWORD:
            print "Nombre de usuario o password incorrectos."
            self.password = None
        elif process.returncode == TSMClient.TSM_UNEXPECTED_SQL:
            print "Sentencia SQL incorrecta, consulte el log para obtener detalles."

    def getNodeNameFromIP(self, ip):
        query = "select NODE_NAME from nodes where TCP_ADDRESS='%s'" % ip
        parser = TSM_CSVSelectParser()
        self.run_TSM_CSV_Command(query, parser.parse)
        if len(parser.data) == 1:
            return parser.data[0][0]
        return None

    def getIPFromNodeName(self, node_name):
        query = "select TCP_ADDRESS from nodes where NODE_NAME='%s'" % node_name
        parser = TSM_CSVSelectParser()
        self.run_TSM_CSV_Command(query, parser.parse)
        if len(parser.data) == 1:
            return parser.data[0][0]
        return None

    def getNodeEvents(self, node, since):
        """
         tsm: BACKUP-SAN_SERVER1>select * from events where
         scheduled_start>'2010-05-27 0:0:0' and node_name='VMWSUS' and status <>
         'Future'

0         SCHEDULED_START: 2010-05-27 22:00:00.000000
1            ACTUAL_START: 2010-05-27 22:09:20.000000
2             DOMAIN_NAME: DIARIA
3           SCHEDULE_NAME: DIARIA
4               NODE_NAME: VMWSUS
5                  STATUS: Completed
6                  RESULT: 0
7                  REASON:
8               COMPLETED: 2010-05-27 22:10:24.000000
        """
        since_str = since.strftime('%Y-%m-%d %H:%M:%S')
        query = "select * from events where scheduled_start>'%s' and node_name='%s' and status <> 'Future'" % (since_str, node) 
        parser = TSM_CSVSelectParser()
        self.run_TSM_CSV_Command(query, parser.parse)
        return parser.data

    def getBackupInformation(self, node_name, since):
        since_date_str = since.strftime('%m/%d/%Y')
        since_time_str = since.strftime('%H:%M:%S')
        since_time_str = '00:00:00'
        query = "query actlog node=%s begindate='%s' begintime='%s' originator=client msgno=4952" % (
                node_name,
                since_date_str,
                since_time_str
            )
        parser = TSM_CSVSelectParser()
        self.run_TSM_CSV_Command(query, parser.parse)
        backups = []
        for backup in parser.data:
            bckp = {}
            bckp['start time'] = backup[0]
            log_msg = backup[1].split()
            session_no = int(log_msg[-1][:-1])
            bckp['session'] = session_no
            bckp['objects inspected'] = int(log_msg[-3].replace('.', '').replace(',', ''))
            query = "query actlog node=%s begindate='%s' begintime='%s' originator=client SESSNUM=%d" % (
                    node_name,
                    since_date_str,
                    since_time_str,
                    session_no
                )
            session_parser = TSM_CSVSelectParser()
            self.run_TSM_CSV_Command(query, session_parser.parse)
            for info in session_parser.data:
                key = None
                if info[1].startswith('ANE4954I'):
                    key = 'objects backed up'
                elif info[1].startswith('ANE4957I'):
                    key = 'objects deleted'
                elif info[1].startswith('ANE4958I'):
                    key = 'objects updated'
                elif info[1].startswith('ANE4959I'):
                    key = 'objects failed'
                elif info[1].startswith('ANE4960I'):
                    key = 'objects rebound'
#                elif info[1].startswith('ANE4961I'):
#                    key = 'bytes transferred'
                elif info[1].startswith('ANE4965I'):
                    key = 'subfile objects'
                elif info[1].startswith('ANE4970I'):
                    key = 'objects expired'
                if key:
                    numero = info[1].split()[-3].replace('.', '').replace(',', '')
                    bckp[key] = int(numero)
            backups.append(bckp)
        return backups

    def getArchiveInformation(self, node_name, since):
        """
             NODE_NAME: VCVMWARE
FILESPACE_NAME: \\vcvmware\d$
  FILESPACE_ID: 5
          TYPE: FILE
       HL_NAME: \VMSNAPSHOTS\APPDB.GES.CCTI.ULL.ES-FULLVM\
       LL_NAME: SCSI0-0-0-APPDB-S004.VMDK
     OBJECT_ID: 277878269
  ARCHIVE_DATE: 2010-05-28 21:31:57.000000
         OWNER: 
   DESCRIPTION: 20100528 FullVM en VCVMWARE
    CLASS_NAME: ARCHIVE90D

        """
        query = "select * from archives where TYPE=FILE and NODE_NAME='%s' and YEAR(ARCHIVE_DATE)>=%d and MONTH(ARCHIVE_DATE)>=%d and DAY(ARCHIVE_DATE)>=%d order by archive_date" % (
                node_name,
                since.year,
                since.month,
                since.day
            )
        parser = TSM_CSVSelectParser()
        self.run_TSM_CSV_Command(query, parser.parse)
        backups = []
        for backup in parser.data:
            fecha = datetime.datetime(*time.strptime(backup[7].split('.')[0], '%Y-%m-%d %H:%M:%S')[0:5])
            b = {
                    'fecha': fecha,
                    'fichero':backup[4] + backup[5],
                    'filespace':backup[1],
                    'description':backup[9]
                }
            backups.append(b)
        return backups

if __name__ == "__main__":
#    print "hola"
    num_dias = 90
    hoy = datetime.datetime.now()
    fecha_anterior = hoy - datetime.timedelta(days = num_dias)
    fecha_anterior = datetime.datetime(2009, 1, 1)
    tsm = TSMClient()
    parser = TSM_CSVSelectParser()
    tsm.setDsmcPath('/opt/tivoli/tsm/client/ba/bin/')
    tsm.setUsername('admin')
    backups = tsm.getArchiveInformation('VCVMWARE', fecha_anterior)
    for b in backups:
        dia_uno, max_dias = calendar.monthrange(b['fecha'].year, b['fecha'].month)
        max_dias -= 8
        if (b['fecha'].month == 2) and (b['fecha'].year == 2010):
            continue
        if b['fichero'].find('GESWIFI.COM.CCTI.ULL.ES') >= 0:
#            print "Geswifi!!! no se borra ... %s --> %s" % (b['fecha'], b['fichero'])
            continue
        if b['description'].find('20100430') >= 0:
#            print "Las copias de abril terminaron en mayo!!! no se borra ... %s --> %s" % (b['fecha'], b['fichero'])
            continue
        if (b['fecha'].year == hoy.year and b['fecha'].month == hoy.month) or (b['fecha'].day > max_dias):
            continue
#        print "Borrar: %s --> %s" % (b['fecha'], b['fichero'])
        print "Fecha: %s" % b['fecha']
        print "delete archive -noprompt -description=\"%s\" %s%s" % (b['description'], b['filespace'], b['fichero'])
#        print "delete archive -pick -description=\"%s\" %s%s" % (b['description'], b['filespace'], b['fichero'])
