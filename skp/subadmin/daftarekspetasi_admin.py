from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from skp.models import DaftarEkspetasi, PerilakuKerja


class DaftarEkspetasiAdmin(admin.ModelAdmin):
    list_display = ("pk", "perilaku_kerja", "get_ekspetasi", "created", "is_active")

    def get_ekspetasi(self, obj):
        if obj.ekspetasi and len(obj.ekspetasi) > 70:
            return obj.ekspetasi[:67] + "..."
        return obj.ekspetasi

    get_ekspetasi.short_description = "Ekspetasi"

    def load(self, request):
        perilaku_id = request.GET.get("perilaku_id", None)
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        if perilaku_id:
            try:
                perilaku_obj = PerilakuKerja.objects.get(pk=perilaku_id)
            except PerilakuKerja.DoesNotExist:
                respon = {"success": False, "pesan": "Perilaku Kerja Tidak ditemukan"}
                return JsonResponse(respon, safe=False)
            else:
                data = []
                find_daftar = DaftarEkspetasi.objects.filter(
                    perilaku_kerja=perilaku_obj
                )
                if find_daftar.exists():
                    find_daftar = find_daftar.order_by("ekspetasi")
                    for i in find_daftar:
                        data.append({"id": i.id, "nama": i.ekspetasi})
                respon = {"success": True, "data": data}
        else:
            respon = {"success": False, "pesan": "Perilaku Kerja dibutuhkan"}
        return JsonResponse(respon, safe=False)

    def get_urls(self):
        admin_url = super(DaftarEkspetasiAdmin, self).get_urls()
        custom_url = [
            path(
                "load/",
                self.admin_site.admin_view(self.load),
                name="daftar-ekspetasi-load",
            ),
        ]
        return custom_url + admin_url
