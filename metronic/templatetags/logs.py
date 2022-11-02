from django import template
from django.contrib.admin.models import LogEntry

# import datetime
# from dateutil.relativedelta import relativedelta
register = template.Library()


@register.filter(name="get_logs")
def get_logs(user, total_):
    if user.is_superuser:
        logs = LogEntry.objects.all()
    elif not user.is_anonymous():
        logs = LogEntry.objects.filter(user=user)
    else:
        logs = LogEntry.objects.none()
    if total_:
        return [logs[:total_], logs.count()]
    else:
        return [logs, logs.count()]
