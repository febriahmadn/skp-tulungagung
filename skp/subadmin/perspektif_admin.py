from django.contrib import admin


class PerspektifAdmin(admin.ModelAdmin):
    list_display = ("pk", "perspektif", "created")
