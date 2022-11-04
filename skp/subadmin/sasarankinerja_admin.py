from django.contrib import admin


class SasaranKinerjaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pegawai', 'get_unor', 'jabatan', 'pejabat_penilai', 'periode_awal', 'periode_akhir', 'pendekatan', 'status')

    def get_unor(self, obj):
        if obj.unor:
            return obj.unor
        elif obj.unor_text:
            return obj.unor_text
        return ''
    get_unor.short_description = 'Unor'
