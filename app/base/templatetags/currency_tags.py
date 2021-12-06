import math
from django import template

register = template.Library()


@register.filter
def divide_by_100(value):
    """
    TODO: This should be part of a currency model with class methods (@property).
    Used to convert from øre to NOK i MVP
    """
    if not value:
        raise ValueError('divide_by_100 needs a number!')
    return math.ceil(value / 100)


@register.filter
def global_raise_value(value):
    """"
    TODO: For mvp purposes only
    This should be a model or a function calculating the raise in bid's
    i.e an auction lower than 1000 should raise by 50 and higher than by 100,
    or set by store...
    """
    if not value:
        raise ValueError('global_raise_value needs a number')
    return value + 5
