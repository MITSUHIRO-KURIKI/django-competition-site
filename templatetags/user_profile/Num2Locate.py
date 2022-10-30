from django import template
from user_profile.models import (
    LOCATE_CHOICES,
)


register = template.Library()


locate_dict = dict( (k,v) for k,v in LOCATE_CHOICES() )
@register.filter
def num2locate(num):
    locate = locate_dict[num]
    return locate