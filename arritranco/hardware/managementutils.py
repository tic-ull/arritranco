'''
Created on 31/05/2011

@author: Agustin
'''
from pysnmp.entity.rfc3413.oneliner import cmdgen
import paramiko

SNMP_OID_SysDescr = (1,3,6,1,2,1,1,1,0)
SNMP_OID_sysName = (1,3,6,1,2,1,1,5,0)
SNMP_OID_sysLocation = (1,3,6,1,2,1,1,6,0)

#returns (errorDescription, value)
def snmpV1GetSingleValue(hostname, readcommunity, mib):
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
        #SNMPv1                                                                                  
        cmdgen.CommunityData('arritranco-agent', readcommunity, 0),
        # Transport
        cmdgen.UdpTransportTarget((hostname, 161)),
        # Variables
        mib
    )

    errordesc = None
    if errorIndication:
        errordesc = errorIndication
    elif errorStatus:
        errordesc = '%s at %s\n' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
    else:
        #No he comprobado si varBinds esta vacia
        return None, varBinds[0][1]
    return errordesc, None

#returns errorDescription
def sftpGet(hostname, username, password, sourcefile, destfile, port = 22):
    # connect and use paramiko Transport to negotiate SSH2 across the connection
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(sourcefile, destfile)
        t.close()
        return None
    
    except Exception, e:
        try:
            t.close()
        except:
            pass
        return "SFTP error:%s" % e
        