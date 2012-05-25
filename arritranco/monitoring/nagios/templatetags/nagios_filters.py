from django import template

register = template.Library()

@register.filter
def ostype(value, arg):
    """Returns a list with the nagios checks opts having 'ostype' supplied in 'arg' parameter."""
    rlist = []
    for nco in value:
        if nco['ostype'] == arg:
            rlist.append(nco)
    return rlist
