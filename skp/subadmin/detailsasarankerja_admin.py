from django.contrib import admin


class DetailsasarankerjaAdmin(admin.ModelAdmin):
    list_display=('pk','nama_pegawai','nip_pegawai','golongan_pegawai','jabatan_pegawai','unor_pegawai','nama_pejabat','nip_pejabat','golongan_pejabat','jabatan_pejabat','unor_pejabat')