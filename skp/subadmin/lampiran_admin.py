from django.contrib import admin

class LampiranAdmin(admin.ModelAdmin):
    list_display = ('pk','lampiran','status','created')