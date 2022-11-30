from django.contrib import admin
from django.urls import path, reverse_lazy
from django.http import JsonResponse
from skp.models import (
    RencanaHasilKerja,
    SasaranKinerja,
    IndikatorKinerjaIndividu,
)


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
    search_fields = ("rencana_kerja", "skp__pegawai__nama_lengkap")

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

    def get_data_by_skp(self, request, obj_id):
        # kalau bisa nanti diubah ke rest api lebih bagus
        respon = []
        jenis = request.GET.get("jenis", None)
        try:
            obj = SasaranKinerja.objects.get(pk=obj_id)
        except SasaranKinerja.DoesNotExist:
            pass
        else:
            rencanakerja_list = obj.rencanahasilkerja_set.filter(jenis=jenis).order_by(
                "id"
            )
            if rencanakerja_list.exists():
                for item in rencanakerja_list:
                    rencana_kerja_induk = None
                    if item.induk:
                        rencana_kerja_induk = {
                            "id": item.induk.id,
                            "rencana_kerja": item.induk.rencana_kerja,
                        }
                    indikator = []
                    indikator_list = item.indikatorkinerjaindividu_set.all()
                    if indikator_list.exists():
                        for item_indikator in indikator_list:
                            indikator.append(
                                {
                                    "delete_url": reverse_lazy(
                                        'admin:skp_indikator_hapus', kwargs={
                                            "id": item_indikator.id
                                        }
                                    ),
                                    "indikator_id": item_indikator.id,
                                    "indikator": item_indikator.indikator,
                                    "target": item_indikator.target,
                                    "aspek": item_indikator.aspek,
                                    "perspektif": item_indikator.perspektif.__str__()
                                    if item_indikator.perspektif
                                    else None,
                                }
                            )
                    respon.append(
                        {
                            "id": item.id,
                            "induk": rencana_kerja_induk,
                            "rencana_kerja": item.rencana_kerja,
                            "penugasan_dari": item.penugasan_dari,
                            "indikator": indikator,
                        }
                    )

        return JsonResponse(respon, safe=False)

    def load_rhk_pimpinan(self, request):
        respon = []
        atasan_id = request.user.atasan.id if request.user.atasan else None
        print(atasan_id)
        if atasan_id:
            rhk_list = RencanaHasilKerja.objects.filter(skp__pegawai_id=atasan_id)
            print(rhk_list)
            if rhk_list.exists():
                for item in rhk_list:
                    respon.append(
                        {
                            "id": item.id,
                            "rencana_kerja": item.rencana_kerja,
                        }
                    )
        return JsonResponse(respon, safe=False)

    def set_rhk_pimpinan(self, request):
        rhk_id = request.GET.get("rhk_id", None)
        rhk_pimpinan_id = request.GET.get("rhk_pimpinan_id", None)
        respon = {"success": False}
        if rhk_id and rhk_pimpinan_id:
            try:
                obj = RencanaHasilKerja.objects.get(id=rhk_id)
            except RencanaHasilKerja.DoesNotExist:
                pass
            else:
                obj.induk_id = rhk_pimpinan_id
                obj.save()
                respon = {"success": True}
        return JsonResponse(respon, safe=False)

    def action_add_or_change(self, request):
        respon = {"success": False}
        skp_id = request.POST.get("skp_id", None)
        klasifikasi = request.POST.get("klasifikasi", None)
        unitkerja = request.POST.get("unitkerja", None)
        jenis = request.POST.get("jenis", None)
        rencana_kerja = request.POST.get("rencana_kerja", None)
        penugasan_dari = request.POST.get("penugasan_dari", None)
        try:
            obj = RencanaHasilKerja(
                skp_id=skp_id,
                klasifikasi=klasifikasi,
                unor_id=unitkerja,
                jenis=jenis,
                rencana_kerja=rencana_kerja,
                penugasan_dari=penugasan_dari,
            )
            obj.save()
        except Exception:
            pass
        else:
            respon = {"success": True}
        return JsonResponse(respon, safe=True)

    def get_urls(self):
        urls = super().get_urls()
        urlp = [
            path("load/", self.load_data, name="load-rhk"),
            path(
                "get-data-skp/<int:obj_id>",
                self.admin_site.admin_view(self.get_data_by_skp),
                name="skp_rencarahasilkerja_get_by_skp",
            ),
            path(
                "load-rhk-pimpinan",
                self.admin_site.admin_view(self.load_rhk_pimpinan),
                name="skp_rencanahasilkerja_loadrhkpimpinan",
            ),
            path(
                "set-rhk-pimpinan",
                self.admin_site.admin_view(self.set_rhk_pimpinan),
                name="skp_rencanahasilkerja_set_rhk_pimpinan",
            ),
            path(
                "action-add-or-create",
                self.admin_site.admin_view(self.action_add_or_change),
                name="skp_rencanahasilkerja_action_add_or_change",
            ),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
