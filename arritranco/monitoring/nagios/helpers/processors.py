'''
Created 14/03/2012

@author: alorenzo
'''


def mco2dict(m_chckopts):
    """ Takes a model of NagiosCheckOpts and returns a dict.

        The dict contain necesary opts to render a nagios check
        for the machine:

        - ostype: to take the right check
        - fqdn: the dns name of the server
        - cg: contact groups to recieve alerts
        - has_upsmon: if its a nut check
    """
    rdict = {'ostype': m_chckopts.machine.os.type.name, 'fqdn': m_chckopts.machine.fqdn,
             'cg': m_chckopts.get_ngcontact_groups(), 'options': m_chckopts.options,
             'has_upsmon': m_chckopts.machine.has_upsmon()}
    return rdict


def mco2dict_balanced(m_chckopts, m_balanced):
    """ Takes a model of NagiosCheckOpts and balanced fqdn and returns a dict.

        The dict contain necesary opts to render a nagios check
        for the machine:

        - ostype: to take the right check
        - fqdn: the dns name of the server
        - cg: contact groups to recieve alerts
        - has_upsmon: if its a nut check
    """
    rdict = {'ostype': m_chckopts.machine.os.type.name, 'fqdn': m_balanced.fqdn,
             'cg': m_chckopts.get_ngcontact_groups(), 'options': m_chckopts.options,
             'has_upsmon': m_chckopts.machine.has_upsmon()}
    return rdict

