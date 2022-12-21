import ast

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from skp.models import (DaftarEkspetasi, DaftarPerilakuKerjaPegawai,
                        PerilakuKerja, SasaranKinerja)


def set_daftar_ekspetasi(obj, list_multiple):
    find_ekspetasi = DaftarEkspetasi.objects.filter(pk__in=list_multiple)
    if obj.ekspetasi_tambahan.count() > 0:
        obj.ekspetasi_tambahan.clear()
    for ekp_obj in find_ekspetasi:
        obj.ekspetasi_tambahan.add(ekp_obj)
    obj.save()

class DaftarPerilakuKerjaPegawaiAdmin(admin.ModelAdmin):
    list_display = ("pk", "skp", "perilaku_kerja", "isi", "created")

    def post(self, request):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        skp = request.POST.get('skp_id', None)
        perilaku_id = request.POST.get('perilaku_id', None)
        perilaku_multiple = request.POST.get('perilaku_multiple', None)
        ekspetasi_id = request.POST.get('ekspetasi_id', None)
        isi = request.POST.get('isi', None)
        tambah = False
        try:
            skp_obj = SasaranKinerja.objects.get(pk=skp)
        except SasaranKinerja.DoesNotExist:
            respon = {'success': False, 'pesan': 'Sasaran Kinerja Tidak Ditemukan'}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)

        try:
            perilaku__obj = PerilakuKerja.objects.get(pk=perilaku_id)
        except PerilakuKerja.DoesNotExist:
            respon = {'success': False, 'pesan': 'Data Tidak Ditemukan'}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)

        try:
            obj = DaftarPerilakuKerjaPegawai.objects.get(pk=ekspetasi_id)
        except Exception as e:
            print(e)
            obj = DaftarPerilakuKerjaPegawai(
                skp=skp_obj,
                perilaku_kerja=perilaku__obj
            )
            tambah = True
        obj.isi = isi
        obj.save()
        list_multiple = ast.literal_eval(perilaku_multiple)
        set_daftar_ekspetasi(obj, list_multiple)

        if tambah:
            respon = {'success': True, 'pesan': "Berhasil Menambah Ekspetasi"}
        else:
            respon = {'success': True, 'pesan': "Berhasil Merubah Ekspetasi"}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super(DaftarPerilakuKerjaPegawaiAdmin, self).get_urls()
        custom_url = [
            path(
                "simpan",
                self.admin_site.admin_view(self.post),
                name="skp_daftarperilakuerjapegawai_post",
            ),
        ]
        return custom_url + admin_url
