from celery import shared_task

from services.models import TaskList


@shared_task
def tasklist_run(id=None):
    obj = TaskList.objects.get(id=id)
    obj.proses()
    return True
