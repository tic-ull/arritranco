#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import getpass
import locale
import urllib2
import urllib
import simplejson as json
import getopt
import socket

from tsmclient import *

URLBASE = 'https://inventario.stic.ull.es/rest/backup/tsm/hosts/'

# Default options
verbose = False
nagios = False
password_file = None
num_dias = 1
hostname = None
manual = False
num_backups = 10000
tivoli_server = None

def usage():
    """
        Print information usage
    """
    print """
Usage: check_nagios_tsm.py [options]

 -v  Verbose.
 -n  Nagios format.
 -h  <hostname/> check host.
 -P  <password file/> Password file.
 -d  <num_dias/> Indica cuantos días tiene en cuenta para buscar eventos. Por defecto es 1 (planificación diaria)
 -m  <backups_esperados /> Se pretende verificar un backup manual, no un backup automático.
 -?  Show help
 -t  Tivoli server
"""

def parseOpts():
    """
        Analiza los argumentos pasados por línea de comandos
    """
    global verbose, nagios, hostname, password_file, num_dias, manual, num_backups, tivoli_server
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vh:n?P:d:m:t:")
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(1)
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o == "-?":
            usage()
            sys.exit(0)
        elif o == "-h":
            hostname = a
        elif o == "-n":
            nagios = True
        elif o == "-P":
            password_file = a
        elif o == "-d":
            num_dias = int(a)
        elif o == "-m":
            manual = True
            num_backups = int(a)
        elif o == "-t":
            tivoli_server = str(a)

def get_node_name(hostname = None, ip = None):
    """
        Intenta obtener por todos los medios el nombre del nodo de TSM
    """
    if ip:
        nodo = tsm.getNodeNameFromIP(ip)
        if nodo:
            return nodo
    if hostname:
        ip = tsm.getIPFromNodeName(hostname.upper())
        if ip:
            return hostname.upper()
        nueva_ip = socket.gethostbyname(hostname)
        if nueva_ip != ip:
            return get_node_name(ip = nueva_ip)
    return None

def chequea_nodo(nodo, fecha_anterior, maquina):
    global verbose, nagios

    fallo = False
    eventos = tsm.getNodeEvents(nodo, fecha_anterior)
    if not len(eventos):
        if verbose:
            print "Error, no hay eventos para el rango de fechas"
    else:
        num_fallos = 0
        for row in eventos:
            if row[5] != 'Completed':
                num_fallos += 1
                if not fallo:
                    fallo = True
                    if verbose:
                        print "  Error en la planificación: %s" % row[5]
                        print "    Resultado: %s" % row[6]
                        print "    Razon: %s" % row[7]
    if not fallo:
        if verbose:
            print "OK"
        if nagios:
            print "%s\tTSM Backup %s\t0\tCompleted" % (maquina, maquina)
    else:
        if verbose:
            print "    %s fallos detectados" % num_fallos
        if nagios:
            print "%s\tTSM Backup %s\t2\t%s errores detectados. Revise la interfaz de administracion" % (maquina, maquina, num_fallos)
    return (not fallo)

def chequea_inventario(maquinas, fecha_anterior):
    global verbose

    nodos_inventario  = []
    for maquina in maquinas:
        nodo = get_node_name(maquina['fqdn'].upper(), maquina['ipaddress'])
        if not nodo:
            if verbose:
                print "  - Imposible obtener el nodo de la IP: %s" % maquina['ipaddress']
                print "  - Imposible obtener nodo del: %s" % maquina['fqdn']
            continue
        if verbose:
            print "Obteniendo estado de: %s" % nodo,
        chequea_nodo(nodo, fecha_anterior, maquina['fqdn'])
        nodos_inventario.append(nodo)
    return nodos_inventario

def chequea_tsm(fecha_anterior, nodos_inventario):
    global verbose

    nodos_TSM = []
    tsm.run_TSM_CSV_Command ('query node', parser.parse)
    for nodo in parser.data:
        nodo = nodo[0]
        if verbose:
            print "Obteniendo estado de: %s" % nodo,
        ip = tsm.getIPFromNodeName(nodo)
        try:
            hostname = socket.gethostbyaddr(ip)
        except socket.herror, e:
            hostname = ip
        chequea_nodo(nodo, fecha_anterior, hostname)
        if nodo not in nodos_inventario:
            nodos_TSM.append(nodo)
    return nodos_TSM

def chequea_backup_manual(nodo, num_backups, fecha_anterior, maquina):
    global verbose, nagios
    backup_found = tsm.getBackupInformation(nodo, fecha_anterior)
    if len(backup_found) < num_backups:
        msg = "Error: %s backups encontrados, esperados %s" % (len(backup_found), num_backups)
        if nagios:
            print "%s\tTSM Backup manual %s\t2\t%s" % (maquina, maquina, msg)
        if verbose:
            print msg
    warning = False
    critical = False
    msg = "%s sesiones encontradas: " % len(backup_found)
    for backup in backup_found:
        if backup['objects failed'] < 0.1 *  backup['objects inspected']:
            msg += "Session %s OK: %% de fallos dentro de lo esperado: %s fallos, %s inspeccionados. " % (
                            backup['session'],
                        backup['objects failed'],
                        backup['objects inspected']
                    )
            if verbose:
                print "Ok"
            continue
        else:
            if backup['objects failed'] > 0.3 *  backup['objects inspected']:
                msg += "Session %s CITICAL: %% de fallos _MUY_ superior a lo esperado: %s fallos, %s inspeccionados. "  % (
                            backup['session'],
                            backup['objects failed'],
                            backup['objects inspected']
                        )
                if verbose:
                    print "Critical"
                critical = True
            else:
                msg += "Session %s WARNING: %% de fallos superior a lo esperado: %s fallos, %s inspeccionados. "  % (
                            backup['session'],
                            backup['objects failed'],
                            backup['objects inspected']
                        )
                if verbose:
                    print "Warning"
                warning = True
    if warning:
        if critical:
            if nagios:
                print "%s\tTSM Backup manual %s\t2\t%s" % (maquina, maquina, msg)
            if verbose:
                print msg
        else:
            if nagios:
                print "%s\tTSM Backup manual %s\t1\t%s" % (maquina, maquina, msg)
            if verbose:
                print msg
    else:
        if nagios:
            print "%s\tTSM Backup manual %s\t0\t%s" % (maquina, maquina, msg)
        if verbose:
            print msg

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
    parseOpts()

    tsm = TSMClient(dsmcPath = '/opt/tivoli/tsm/client/ba/bin/', username = 'admin', server = tivoli_server)
    parser = TSM_CSVSelectParser()

    if password_file:
        tsm.setPassword(open(password_file, 'r').read().strip())

    fecha_anterior = datetime.datetime.now() - datetime.timedelta(days = num_dias)
    if hostname:
        nodo = get_node_name(hostname = hostname)
        if nodo:
            if manual:
                chequea_backup_manual(nodo, num_backups, fecha_anterior, hostname)
            else:
                chequea_nodo(nodo, fecha_anterior, hostname)
        sys.exit(0)

    try:
        hosts_url = URLBASE + '?' + urllib.urlencode({'tsm_server':tivoli_server})
        request = urllib2.Request(hosts_url, None, {'Accept': 'application/json'})
        res = urllib2.urlopen(request)
    except Exception, e:
        print e
        raise e

    if nagios:
        chequea_inventario(json.load(res), fecha_anterior)
        sys.exit(0)

    if verbose:
        print " ----------------- Escaneando nodos del inventario ------------------------------"
    nodos_inventario = chequea_inventario(json.load(res), fecha_anterior)
    if verbose:
        print " ----------------- Escaneando nodos del tsm ------------------------------"
    nodos_TSM = chequea_tsm(fecha_anterior, nodos_inventario)
    if verbose:
        print "Nodos en TSM que no estan en el inventario: ",
        for nodo in nodos_TSM:
            print "%s (%s), " % (nodo, tsm.getIPFromNodeName(nodo))
        print ""
        print "Nodos inventario: ", nodos_inventario
