from django import template
from user_profile.models import (
    GENDER_CHOICES,
)


register = template.Library()


gender_dict = dict( (k,v) for k,v in GENDER_CHOICES() )
@register.filter
def num2gender(num):
    gender = gender_dict[num]
    return gender