from django.contrib import admin


class PerilakukerjaAdmin(admin.ModelAdmin):
    list_display = ("pk", "perilaku_kerja", "status", "created")
