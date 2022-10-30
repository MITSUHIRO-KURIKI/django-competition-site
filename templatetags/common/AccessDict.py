from django import template


register = template.Library()


@register.simple_tag
def access_dict(dict_, arg, default=""):
    if arg in dict_:
        return dict_[arg]
    else:
        return default