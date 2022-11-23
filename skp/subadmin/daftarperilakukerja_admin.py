from django.contrib import admin


class DaftarperilakukerjaAdmin(admin.ModelAdmin):
    list_display = ("pk", "perilaku_kerja", "keterangan", "is_active", "created")
