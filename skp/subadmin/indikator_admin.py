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
                        respon.append({
                            'id': item.id,
                            'indikator': item.indikator,
                            'target': item.target,
                            'aspek': item.aspek,
                        })
        return JsonResponse(respon, safe=False)

    def action_save_indikator_rhk(self, request):
        respon = {'success': False}
        rhk_id = request.POST.get('rhk_id', None)
        aspek = request.POST.get('aspek', None)
        indikator = request.POST.get('indikator', None)
        target = request.POST.get('target', None)
        try:
            IndikatorKinerjaIndividu.objects.create(
                rencana_kerja_id=rhk_id,
                aspek=aspek,
                indikator=indikator,
                target=target,
            )
            respon = {'success': True}
        except Exception:
            pass
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        urls = super().get_urls()
        urlp = [
            path("load/", self.load_data, name="load-indikator"),
            path('get-by-skp/<int:obj_id>', self.admin_site.admin_view(self.get_indikator_by_skp), name='skp_indikator_get_by_skp'),
            path('set-rhk', self.admin_site.admin_view(self.action_save_indikator_rhk), name='skp_indikator_set_indikator_rhk'),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
