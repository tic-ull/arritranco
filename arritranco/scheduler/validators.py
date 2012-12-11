# coding: utf-8
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

NOT_IN_RANGE_ERROR = _(u'%s is not in allowed range [%s]')

def build_samples(start, end, wildchar = '*'):
    """Used to build an array of samples to validate the fields on task scheduling."""
    return [ str(x) if len(str(x)) > 1  else '0'+str(x) for x in range(start,end)] + [wildchar]

def validate_month(value):
    allowed_values = build_samples(1,13)
    if value not in allowed_values:
        raise ValidationError(NOT_IN_RANGE_ERROR % (value, ','.join(allowed_values)))

def validate_day_of_month(value):
    allowed_values = build_samples(1,32)
    if value not in allowed_values:
        raise ValidationError(NOT_IN_RANGE_ERROR % (value, ','.join(allowed_values)))

def validate_day_of_week(value):
    allowed_values = build_samples(0,8) # 0 = sunday
    if value not in allowed_values:
        raise ValidationError(NOT_IN_RANGE_ERROR % (value, ','.join(allowed_values)))

def validate_hour(value):
    allowed_values = build_samples(0,24)
    if value not in allowed_values:
        raise ValidationError(NOT_IN_RANGE_ERROR % (value, ','.join(allowed_values)))

def validate_minute(value):
    allowed_values = build_samples(0,60)
    if value not in allowed_values:
        raise ValidationError(NOT_IN_RANGE_ERROR % (value, ','.join(allowed_values)))

