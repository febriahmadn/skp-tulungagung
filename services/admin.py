from django.contrib import admin
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin

from services.models import Configurations, TaskList

admin.site.register(Configurations, SingletonModelAdmin)


class TaskListAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "jenis_task",
        "parameter",
        "presentase",
        "is_done",
        "button_action",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ("jenis_task", "parameter"),
            },
        ),
    )

    def button_action(self, obj):
        str_html = ""
        if obj.is_done:
            str_html = """
            <button class="btn btn-success btn-sm">Done</button>
            """
        else:
            str_html = """
            <button class="btn btn-warning btn-sm">Proses</button>
            """
        return mark_safe(str_html)

    button_action.short_description = "Action"


admin.site.register(TaskList, TaskListAdmin)
