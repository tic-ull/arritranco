# -*- coding: utf-8 -*-

from django import template
import re

register = template.Library()

@register.filter
def ostype(value, arg):
    """Returns a list with the nagios checks opts having 'ostype' supplied in 'arg' parameter."""
    rlist = []
    for nco in value:
        if arg[0] == '!' and nco['ostype'] != arg[1:]:
            rlist.append(nco)
        elif nco['ostype'] == arg:
            rlist.append(nco)
    return rlist

@register.filter
def nagios_safe(value):
    out = unicode(value)
    out = out.replace(u"\t", " ")
    out = out.replace(u"á", "a").replace(u"é", "e").replace(u"í", "i").replace(u"ó", "o").replace(u"ú", "u")
    out = out.replace(u"Á", "A").replace(u"É", "E").replace(u"Í", "I").replace(u"Ó", "O").replace(u"Ú", "U")
    out = re.sub(r'[^A-Za-z0-9: ]', r'?', out)
    out = out.replace(u"?", "")
    out = out.replace(u"  ", " ")
    return out[:63].strip()
