from django.contrib import admin


class IndikatorAdmin(admin.ModelAdmin):
    list_display = ("pk", "rencana_kerja", "indikator", "target", "perspektif")
