from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from skp.models import IndikatorKinerjaIndividu, SasaranKinerja


class IndikatorAdmin(admin.ModelAdmin):
    list_display = ("pk", "rencana_kerja", "indikator", "target", "aspek", "perspektif")

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

    def get_indikator_by_skp(self, request, obj_id):
        respon = []
        try:
            obj = SasaranKinerja.objects.get(pk=obj_id)
        except SasaranKinerja.DoesNotExist:
            pass
        else:
            indikator_list = obj.indikatorkinerjaindividu_set.all()
            if indikator_list.exists():
                for item in indikator_list:
                    if item.rencana_kerja is None:
                        respon.append(
                            {
                                "id": item.id,
                                "indikator": item.indikator,
                                "target": item.target,
                                "aspek": item.aspek,
                            }
                        )
        return JsonResponse(respon, safe=False)

    def action_save_indikator_rhk(self, request):
        respon = {"success": False}
        indikator_id = request.POST.get("indikator_id", None)
        rhk_id = request.POST.get("rhk_id", None)
        aspek = request.POST.get("aspek", None)
        perspektif = request.POST.get("perspektif", None)
        indikator = request.POST.get("indikator", None)
        target = request.POST.get("target", None)

        if indikator_id and indikator_id != "":
            try:
                obj = IndikatorKinerjaIndividu.objects.get(pk=indikator_id)
            except IndikatorKinerjaIndividu.DoesNotExist:
                respon = {"success": False}
                return JsonResponse(respon, safe=False)
        else:
            obj = IndikatorKinerjaIndividu(
                rencana_kerja_id=rhk_id,
            )
        obj.aspek = aspek
        obj.indikator = indikator
        obj.target = target

        if perspektif:
            if perspektif != "0" or perspektif != 0:
                obj.perspektif_id = perspektif
        obj.save()
        respon = {"success": True}
        return JsonResponse(respon, safe=False)

    def indikator_delete(self, reqeust, id):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        try:
            obj = IndikatorKinerjaIndividu.objects.get(pk=id)
        except IndikatorKinerjaIndividu.DoesNotExist:
            respon = {'success': False, 'pesan': "Indikator Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {'success': True, 'pesan': "Berhasil Menghapus Indikator"}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        urls = super().get_urls()
        urlp = [
            path("load/", self.load_data, name="load-indikator"),
            path(
                "get-by-skp/<int:obj_id>",
                self.admin_site.admin_view(self.get_indikator_by_skp),
                name="skp_indikator_get_by_skp",
            ),
            path(
                "set-rhk",
                self.admin_site.admin_view(self.action_save_indikator_rhk),
                name="skp_indikator_set_indikator_rhk",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.indikator_delete),
                name="skp_indikator_hapus",
            ),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
