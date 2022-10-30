from django import template


register = template.Library()


@register.filter
def split_slash_text(text):
    # USE {{ TEXT  | split_slash_text | last }}
    text = str(text)
    split_slash_text_list = text.split('/')
    return split_slash_text_list

@register.simple_tag
def split_blank_text(text):
    text = str(text)
    try:
        split_blank_text_list = text.split(' ')
    except:
        split_blank_text_list = None
    return split_blank_text_list