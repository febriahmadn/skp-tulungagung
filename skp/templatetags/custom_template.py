from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def state_show(param=None):
    if len(param) > 0:
        return True
    return False

@register.filter
def selected_jenis(first, second):
    if second.GET.get("jenis_statistik"):
        if str(first) == str(second.GET.get("jenis_statistik")):
            return "selected"
    return ""

@register.filter
def selected_tahun(first, second):
    if second.GET.get("tahun"):
        if str(first) == str(second.GET.get("tahun")):
            return "selected"
    return ""
