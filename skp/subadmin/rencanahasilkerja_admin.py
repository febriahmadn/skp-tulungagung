from django.contrib import admin


class RencanahasilkerjaAdmin(admin.ModelAdmin):
    list_display=('pk','skp','rencana_kerja','penugasan_dari','jenis','klasifikasi','unor')