from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from skp.models import DaftarLampiran, Lampiran, SasaranKinerja
class DaftarlampiranAdmin(admin.ModelAdmin):
    list_display = ("pk", "lampiran", "isi", "created")

    def post(self, request):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        skp_obj = None
        lampiran_obj = None

        skp = request.POST.get('skp_id')
        lampiran_id = request.POST.get('lampiran')
        isi = request.POST.get('isi')
        edit = request.POST.get('edit')
        if edit == "false":
            model = Lampiran
        else:
            model = DaftarLampiran

        try:
            lampiran_obj = model.objects.get(pk=lampiran_id)
        except model.DoesNotExist:
            respon = {'success': False, 'pesan': 'Data Tidak Ditemukan'}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)

        try:
            skp_obj = SasaranKinerja.objects.get(pk=skp)
        except SasaranKinerja.DoesNotExist:
            respon = {'success': False, 'pesan': 'Sasaran Kinerja Tidak Ditemukan'}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)

        if skp_obj and lampiran_obj:
            if edit == 'false':
                daftar_obj = DaftarLampiran(
                    lampiran=lampiran_obj,
                    skp=skp_obj,
                    isi=isi
                )
                daftar_obj.save()
            else:
                lampiran_obj.isi = isi
                lampiran_obj.save()
            respon = {'success': True, 'pesan': 'Berhasil Menyimpan Data Lampiran'}
        return JsonResponse(respon, safe=False)

    def daftar_lampiran_delete(self, reqeust, id):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        try:
            obj = DaftarLampiran.objects.get(pk=id)
        except DaftarLampiran.DoesNotExist:
            respon = {'success': False, 'pesan': "Lampiran Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {'success': True, 'pesan': "Berhasil Menghapus Lampiran"}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super(DaftarlampiranAdmin, self).get_urls()
        custom_url = [
            path(
                "simpan",
                self.admin_site.admin_view(self.post),
                name="skp_daftarlampiran_post",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.daftar_lampiran_delete),
                name="skp_daftarlampiran_hapus",
            ),
        ]
        return custom_url + admin_url
