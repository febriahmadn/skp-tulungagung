from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, reverse_lazy

from skp.models import (BuktiDukung, IndikatorKinerjaIndividu, Realisasi,
                        RencanaAksi, RencanaHasilKerja, SasaranKinerja)

def rencana_aksi_list(skp_obj, rhk_obj, periode):
    rencana_aksi = []
    if periode and periode != "":
        rencana_aksi_list = RencanaAksi.objects.filter(
            skp=skp_obj, rhk=rhk_obj, periode=int(periode)
        )
        for rencana_item in rencana_aksi_list:
            rencana_aksi.append(rencana_item.rencana_aksi)
    return rencana_aksi

def bukti_dukung_list(skp_obj, rhk_obj, periode):
    bukti_dukung = []
    if periode and periode != "":
        bukti_dukung_list = BuktiDukung.objects.filter(
            skp=skp_obj, rhk=rhk_obj, periode=int(periode)
        )
        for bukti_item in bukti_dukung_list:
            bukti_dukung.append({
                "delete_url": reverse_lazy(
                    "admin:skp_buktidukung_hapus", kwargs={
                        "id": bukti_item.id
                    }
                ),
                "id": bukti_item.id,
                "nama": bukti_item.nama_bukti_dukung,
                "link": bukti_item.link,
            })
    return bukti_dukung

def realisasi_list(skp_obj, rhk_obj, periode):
    realisasi = []
    if periode and periode != "":
        realisasi_list = Realisasi.objects.filter(
            skp=skp_obj, rhk=rhk_obj, periode=int(periode)
        )
        for realisasi_item in realisasi_list:
            realisasi.append({
                "delete_url": reverse_lazy(
                    "admin:skp_realisasi_hapus", kwargs={
                        "id": realisasi_item.id
                    }
                ),
                "id": realisasi_item.id,
                "realisasi": realisasi_item.realisasi,
                "sumber": realisasi_item.sumber,
            })
    return realisasi


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
        status_edit = request.GET.get("edit", False)
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
                if status_edit == "true":
                    data = {
                        'id': obj.id,
                        'rencana_hasil': obj.rencana_kerja,
                        'penugasan_dari': obj.penugasan_dari,
                        'jenis': obj.jenis,
                        'klasifikasi': obj.klasifikasi,
                        'unor': obj.unor.id if obj.unor else None,
                        'aspek': obj.aspek
                    }
                else:
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
        periode = request.GET.get("periode", None)
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
                            "delete_url": reverse_lazy(
                                'admin:skp_rhk_hapus', kwargs={
                                    "id": item.id
                                }
                            ) if len(indikator) <= 0 else "",
                            "id": item.id,
                            "induk": rencana_kerja_induk,
                            "rencana_kerja": item.rencana_kerja,
                            "rencana_aksi": rencana_aksi_list(obj, item, periode),
                            "realisasi": realisasi_list(obj, item, periode),
                            "penugasan_dari": item.penugasan_dari,
                            "indikator": indikator,
                            "bukti_dukung": bukti_dukung_list(obj, item, periode),
                        }
                    )

        return JsonResponse(respon, safe=False)

    def load_rhk_pimpinan(self, request):
        respon = []
        atasan_id = request.user.atasan.id if request.user.atasan else None
        if atasan_id:
            rhk_list = RencanaHasilKerja.objects.filter(skp__pegawai_id=atasan_id)
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
        rhk_id = request.POST.get("rhk_id", None)
        skp_id = request.POST.get("skp_id", None)
        klasifikasi = request.POST.get("klasifikasi", None)
        unitkerja = request.POST.get("unitkerja", None)
        jenis = request.POST.get("jenis", None)
        rencana_kerja = request.POST.get("rencana_kerja", None)
        penugasan_dari = request.POST.get("penugasan_dari", None)
        if rhk_id and rhk_id != "":
            try:
                obj = RencanaHasilKerja.objects.get(pk=rhk_id)
            except RencanaHasilKerja.DoesNotExist:
                obj = RencanaHasilKerja(
                    skp_id=skp_id
                )
            except Exception as e:
                respon = {"success": False, 'pesan': str(e)}
                return JsonResponse(respon, safe=False)
        else:
            obj = RencanaHasilKerja(
                skp_id=skp_id
            )

        obj.klasifikasi = klasifikasi
        obj.unor_id = unitkerja
        obj.jenis = int(jenis)
        obj.rencana_kerja = rencana_kerja
        obj.penugasan_dari = penugasan_dari
        obj.save()
        respon = {"success": True}
        return JsonResponse(respon, safe=True)

    def rhk_delete(self, reqeust, id):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        try:
            obj = RencanaHasilKerja.objects.get(pk=id)
        except RencanaHasilKerja.DoesNotExist:
            respon = {'success': False, 'pesan': "Rencana Hasil Kerja Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {
                'success': True,
                'pesan': "Berhasil Menghapus Rencana Hasil Kerja"
            }
        return JsonResponse(respon, safe=False)

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
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.rhk_delete),
                name="skp_rhk_hapus",
            ),
            # path("skpdata/", self.view_custom, name="list_skp_admin"),
            # path("skpdata/add/", self.add_skp, name="add_skp_admin"),
        ]
        return urlp + urls
