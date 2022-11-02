from django import template
register = template.Library()


@register.filter(name='str_remove')
def str_remove(str_, remove_str):
    return str_.replace(remove_str, "")


@register.filter(name='str_petik')
def str_petik(str_):
    return str_.replace('\'', "\\\'")
