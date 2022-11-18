from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from skp.models import RencanaHasilKerja, SasaranKinerja, IndikatorKinerjaIndividu


class RencanahasilkerjaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "skp",
        "rencana_kerja",
        "penugasan_dari",
        "jenis",
        "klasifikasi",
        "unor",
    )

    def load_data(self, request):
        rencana_id = request.GET.get("id", None)
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        if rencana_id:
            try:
                obj = RencanaHasilKerja.objects.get(pk=rencana_id)
            except RencanaHasilKerja.DoesNotExist:
                respon = {
                    "success": False,
                    "pesan": "Rencana Hasil Kerja Tidak Ditemukan",
                }
            except Exception as e:
                respon = {"success": False, "pesan": "Error", "data": str(e)}
            else:
                data = []
                indikator_list = IndikatorKinerjaIndividu.objects.filter(
                    rencana_kerja=obj
                )
                if obj.skp.jenis_jabatan == SasaranKinerja.JenisJabatan.JPT:
                    data = {
                        "jenis": "rhk",
                        "rencana_hasil": obj.rencana_kerja,
                        "jenis_rhk": obj.get_jenis_display(),
                        "indikator_count": indikator_list.count()
                        if indikator_list.count() > 0
                        else 1,
                        "indikator_list_id": list(
                            indikator_list.values_list("id", flat=True)
                        ),
                    }
                respon = {"success": True, "data": data}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        urls = super(RencanahasilkerjaAdmin, self).get_urls()
        urlp = [
            path("load/", self.load_data, name="load-rhk"),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
