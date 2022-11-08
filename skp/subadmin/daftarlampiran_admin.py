from django.contrib import admin

class DaftarlampiranAdmin(admin.ModelAdmin):
    list_display = ('pk','lampiran','isi','created')