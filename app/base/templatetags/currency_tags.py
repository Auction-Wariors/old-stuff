import math
from django import template

register = template.Library()


@register.filter
def divide_by_100(value):
    return math.ceil(value / 100)

