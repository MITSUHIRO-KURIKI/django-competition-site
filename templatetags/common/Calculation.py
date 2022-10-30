from django import template
import numpy as np

register = template.Library()


@register.simple_tag
def calculation_Add(val1, val2):
    try:
        result = val1 + val2
        return result
    except:
        return None

@register.simple_tag
def calculation_Multiplication(val1, val2):
    try:
        result = val1 * val2
        return result
    except:
        return None

@register.simple_tag
def calculation_Division(val1, val2, decimals):
    try:
        result = val1 / val2
        result = np.round(result, decimals=decimals)
        return result
    except:
        return None