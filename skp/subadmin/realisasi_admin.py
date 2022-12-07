from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from skp.models import RencanaHasilKerja, SasaranKinerja, Realisasi


class RealisasiAdmin(admin.ModelAdmin):
    list_display = ("pk", "skp", "rhk", "periode", "realisasi", "sumber", "created")

    def create(self, request):
        respon = {'success': False}
        skp = request.POST.get('skp_id')
        realisasi_id = request.POST.get('realisasi_id')
        periode = request.POST.get('periode')
        rhk = request.POST.get('rhk_id')
        realisasi = request.POST.get('realisasi', None)
        sumber = request.POST.get('sumber', None)

        skp_obj = None
        rhk_obj = None
        if realisasi_id == "":
            realisasi_id = None

        try:
            skp_obj = SasaranKinerja.objects.get(pk=skp)
        except SasaranKinerja.DoesNotExist:
            respon = {'success': False, 'pesan': "SKP Tidak ditemukan"}
            return JsonResponse(respon, safe=False)

        try:
            rhk_obj = RencanaHasilKerja.objects.get(pk=rhk)
        except RencanaHasilKerja.DoesNotExist:
            respon = {'success': False, 'pesan': "RHK Tidak ditemukan"}
            return JsonResponse(respon, safe=False)

        if skp_obj and rhk_obj:
            tambah = True
            try:
                obj = Realisasi.objects.get(pk=realisasi_id)
                tambah = False
            except Exception as e:
                print(e)
                obj = Realisasi(
                    skp=skp_obj,
                    rhk=rhk_obj,
                    periode=int(periode)
                )

            obj.realisasi = realisasi
            obj.sumber = sumber
            obj.save()

            if tambah:
                respon = {'success': True, 'pesan': "Berhasil Menambah Realisasi"}
            else:
                respon = {'success': True, 'pesan': "Berhasil Merubah Realisasi"}
        return JsonResponse(respon, safe=False)

    def realisasi_delete(self, reqeust, id):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        try:
            obj = Realisasi.objects.get(pk=id)
        except Realisasi.DoesNotExist:
            respon = {'success': False, 'pesan': "Realisasi Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {
                'success': True,
                'pesan': "Berhasil Menghapus Realisasi"
            }
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super(RealisasiAdmin, self).get_urls()
        custom_url = [
            path(
                "create",
                self.admin_site.admin_view(self.create),
                name="realisasi-create",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.realisasi_delete),
                name="skp_realisasi_hapus",
            ),
        ]
        return custom_url + admin_url
