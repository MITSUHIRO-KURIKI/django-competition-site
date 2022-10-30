from django import template


register = template.Library()


@register.simple_tag
def access_list(some_list: list, index: int):
    try:
        result = some_list[int(index)]
        return result
    except:
        return ""