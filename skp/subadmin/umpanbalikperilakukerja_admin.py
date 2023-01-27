import ast

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.shortcuts import get_object_or_404

from skp.models import (
    PerilakuKerja,
    UmpanBalik,
    UmpanBalikPerilakuKerja,
    SasaranKinerja,
)


class UmpanBalikPerilakuKerjaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "perilaku_kerja",
        "get_umpan_balik",
        "umpan_balik_tambahan",
        "created",
    )

    def get_umpan_balik(self, obj):
        if obj.umpan_balik.count() > 0:
            html = """<ol style="margin: unset; padding-left: 15px;">"""
            for i in obj.umpan_balik.all():
                html += "<li>{}</li>".format(i.nama)
            html += "</ol>"
            return html
        return "---"

    get_umpan_balik.short_description = "Umpan Balik"

    def create(self, request):
        respon = {"success": False}
        perilaku_kerja = request.POST.get("perilaku_kerja_id")
        umpan_id = request.POST.get("umpan_id")
        skp_id = request.POST.get("skp_id")
        umpan_list = request.POST.get("umpan_list", None)
        umpan_balik_tambahan = request.POST.get("umpan_balik_tambahan", None)

        if umpan_id == "":
            umpan_id = None

        perilaku_obj = get_object_or_404(PerilakuKerja, pk=perilaku_kerja)
        skp_obj = get_object_or_404(SasaranKinerja, pk=skp_id)

        if perilaku_obj:
            tambah = True
            try:
                obj = UmpanBalikPerilakuKerja.objects.get(pk=umpan_id)
                tambah = False
            except Exception:
                obj = UmpanBalikPerilakuKerja(perilaku_kerja=perilaku_obj, skp=skp_obj)
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
                    "pesan": "Berhasil Menambah Umpan Balik Perilaku Kerja",
                }
            else:
                respon = {
                    "success": True,
                    "pesan": "Berhasil Merubah Umpan Balik Perilaku Kerja",
                }
        return JsonResponse(respon, safe=False)

    def umpan_delete(self, reqeust, id):
        respon = {"success": False, "pesan": "Terjadi kesalahan sistem"}
        try:
            obj = UmpanBalikPerilakuKerja.objects.get(pk=id)
        except UmpanBalikPerilakuKerja.DoesNotExist:
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
                name="umpan-balik-perilaku-kerja-craated",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.umpan_delete),
                name="umpan-balik-perilaku-kerja-delete",
            ),
        ]
        return custom_url + admin_url
