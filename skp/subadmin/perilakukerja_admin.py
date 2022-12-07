from django.contrib import admin

from skp.models import DaftarPerilakuKerja


class DaftarPerilakuInline(admin.StackedInline):
    model = DaftarPerilakuKerja
    extra = 0

class PerilakukerjaAdmin(admin.ModelAdmin):
    list_display = ("pk", "perilaku_kerja", "is_active", "created")
    inlines = [
        DaftarPerilakuInline,
    ]
