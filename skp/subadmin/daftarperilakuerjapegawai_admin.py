from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from skp.models import SasaranKinerja, PerilakuKerja, DaftarPerilakuKerjaPegawai

class DaftarPerilakuKerjaPegawaiAdmin(admin.ModelAdmin):
    list_display = ("pk", "skp", "perilaku_kerja", "isi", "created")

    def post(self, request):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        skp = request.POST.get('skp_id', None)
        perilaku_id = request.POST.get('perilaku_id', None)
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
            if ekspetasi_id != "":
                obj = DaftarPerilakuKerjaPegawai.objects.get(pk=ekspetasi_id)
            else:
                obj = DaftarPerilakuKerjaPegawai(
                    skp=skp_obj,
                    perilaku_kerja=perilaku__obj
                )
                tambah = True
        except DaftarPerilakuKerjaPegawai.DoesNotExist:
            obj = DaftarPerilakuKerjaPegawai(
                skp=skp_obj,
                perilaku_kerja=perilaku__obj
            )
            tambah = True
        obj.isi = isi
        obj.save()

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
