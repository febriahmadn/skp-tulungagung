import ast

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from skp.models import IndikatorKinerjaIndividu, UmpanBalik, UmpanBalikPegawai


class UmpanBalikPegawaiAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "indikator",
        "periode",
        "get_umpan_balik",
        "umpan_balik_tambahan",
        "created",
    )

    def get_umpan_balik(self, obj):
        if obj.umpan_balik.count() > 0:
            html = "<ol>"
            for i in obj.umpan_balik.all():
                html += "<li>{}</li>".format(i.nama)
            html += "</ol>"
            return html
        return "---"

    get_umpan_balik.short_description = "Umpan Balik"

    def create(self, request):
        respon = {"success": False}
        indikator = request.POST.get("indikator_id")
        periode = request.POST.get("periode")
        umpan_id = request.POST.get("umpan_id")
        umpan_list = request.POST.get("umpan_list", None)
        umpan_balik_tambahan = request.POST.get("umpan_balik_tambahan", None)

        indikator_obj = None
        if umpan_id == "":
            umpan_id = None

        try:
            indikator_obj = IndikatorKinerjaIndividu.objects.get(pk=indikator)
        except IndikatorKinerjaIndividu.DoesNotExist:
            respon = {"success": False, "pesan": "Indikator Kinerja Tidak ditemukan"}
            return JsonResponse(respon, safe=False)

        if indikator_obj:
            tambah = True
            try:
                obj = UmpanBalikPegawai.objects.get(pk=umpan_id)
                tambah = False
            except Exception:
                obj = UmpanBalikPegawai(indikator=indikator_obj, periode=int(periode))
            obj.umpan_balik_tambahan = umpan_balik_tambahan
            obj.save()

            list_multiple = ast.literal_eval(umpan_list)
            find_umpan = UmpanBalik.objects.filter(pk__in=list_multiple)
            if obj.umpan_balik.count() > 0:
                obj.umpan_balik.clear()
            for umpan_obj in find_umpan:
                obj.umpan_balik.add(umpan_obj)

            if tambah:
                respon = {
                    "success": True,
                    "pesan": "Berhasil Menambah Umpan Balik Pegawai",
                }
            else:
                respon = {
                    "success": True,
                    "pesan": "Berhasil Merubah Umpan Balik Pegawai",
                }
        return JsonResponse(respon, safe=False)

    def umpan_delete(self, reqeust, id):
        respon = {"success": False, "pesan": "Terjadi kesalahan sistem"}
        try:
            obj = UmpanBalikPegawai.objects.get(pk=id)
        except UmpanBalikPegawai.DoesNotExist:
            respon = {"success": False, "pesan": "Umpan Balik Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {"success": False, "pesan": str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {"success": True, "pesan": "Berhasil Menghapus Umpan Balik"}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super().get_urls()
        custom_url = [
            path(
                "create",
                self.admin_site.admin_view(self.create),
                name="umpan-balik-pegawai-crated",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.umpan_delete),
                name="umpan-balik-pegawai-delete",
            ),
        ]
        return custom_url + admin_url
