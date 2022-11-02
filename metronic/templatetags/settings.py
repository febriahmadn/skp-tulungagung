from django import template
# from master.models import Settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='get_setting')
def get_setting(parameter_, default_=None):
    # s = Settings.objects.filter(parameter=parameter_).last()
    s = None
    if s:
        if s.tipe == 'Script':
            return mark_safe(s.value)
        elif s.tipe == "Boolean":
            if s.value == "true":
                return True
            else:
                return False
        else:
            return s.value
    else:
        if default_:
            s = default_
        else:
            s = ""
    return s
