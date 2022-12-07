import base64

from django import template

register = template.Library()


@register.filter(name="debug")
def debug(params, val):
    # print params.filter_specs
    return debug


@register.filter(nama="url_safe_base_64")
def url_safe_base_64(params):
    if params:
        params = base64.urlsafe_b64encode(bytes(params, encoding="utf8"))
    return str(params)
