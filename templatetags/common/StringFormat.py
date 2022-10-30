from django import template


register = template.Library()


@register.simple_tag
def stringformat_s(text):
    text = str(text)
    return text