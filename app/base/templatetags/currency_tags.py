import math
from django import template

register = template.Library()


@register.filter
def divide_by_100(value):
    if not value:
        raise ValueError('divide_by_100 needs a number!')
    return math.ceil(value / 100)


@register.filter
def global_raise_value(value):
    """"
    TODO: This should be a model or a function calculating the raise in bid's
    TODO: i.e an auction lower than 1000 should raise by 50 and higher than by 100 ...
    # No way of having a 2 line t o d o <-- "--><--"
    """
    return value + 5
