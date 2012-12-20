# coding: utf-8
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

NOT_IN_RANGE_ERROR = _(u'%s is not in allowed range [%s]')
UNKNOWN_VALUE = _(u'Unknown value: %s')

def build_samples(start, end, wildchar = '*'):
    """Used to build an array of samples to validate the fields on task scheduling."""
    return range(start,end)

def check(value, allowed):
    values = value.split(',')
    for v in values:
        if v != '*':
            try:
                v = int(v)
            except:
                raise ValidationError(UNKNOWN_VALUE % v)
            if v not in allowed:
                raise ValidationError(NOT_IN_RANGE_ERROR % (v, ','.join(allowed)))

def validate_month(value):
    allowed_values = build_samples(1,13)
    check(value,allowed_values)

def validate_day_of_month(value):
    allowed_values = build_samples(1,32)
    check(value,allowed_values)

def validate_day_of_week(value):
    allowed_values = build_samples(0,8) # 0 and 7 = sunday
    check(value,allowed_values)

def validate_hour(value):
    allowed_values = build_samples(0,24)
    check(value,allowed_values)

def validate_minute(value):
    allowed_values = build_samples(0,60)
    check(value,allowed_values)

