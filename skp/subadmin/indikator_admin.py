from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from skp.models import IndikatorKinerjaIndividu


class IndikatorAdmin(admin.ModelAdmin):
    list_display = ("pk", "rencana_kerja", "indikator", "target", "perspektif")

    def load_data(self, request):
        indikator_id = request.GET.get("id", None)
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        if indikator_id:
            try:
                obj = IndikatorKinerjaIndividu.objects.get(pk=indikator_id)
            except IndikatorKinerjaIndividu.DoesNotExist:
                respon = {
                    "success": False,
                    "pesan": "Rencana Hasil Kerja Tidak Ditemukan",
                }
            except Exception as e:
                respon = {"success": False, "pesan": "Error", "data": str(e)}
            else:
                data = {
                    "jenis": "indikator",
                    "indikator": obj.indikator,
                    "target": obj.target,
                    "perspektif": obj.perspektif.perspektif,
                }
                respon = {"success": True, "data": data}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        urls = super(IndikatorAdmin, self).get_urls()
        urlp = [
            path("load/", self.load_data, name="load-indikator"),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
