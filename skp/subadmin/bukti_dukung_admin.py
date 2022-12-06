from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from skp.models import (
    SasaranKinerja,
    RencanaHasilKerja,
    BuktiDukung,
)

class BuktiDukungAdmin(admin.ModelAdmin):
    list_display = ("pk", "skp", "rhk", "periode", "get_bukti_dukung", "created")

    def get_bukti_dukung(self, obj):
        if self.obj.link and self.obj.link != "":
            return mark_safe('''<a href="{}" target="_blank" >{}</a>'''.format(self.obj.link, self.obj.nama_bukti_dukung))
        return "---"
    get_bukti_dukung.short_description = "Bukti Dukung"

    def create(self, request):
        respon = {'success': False}
        skp = request.POST.get('skp_id')
        bukti_id = request.POST.get('bukti_id')
        periode = request.POST.get('periode')
        rhk = request.POST.get('rhk_id')
        bukti_dukung = request.POST.get('nama', None)
        link = request.POST.get('link', None)

        skp_obj = None
        rhk_obj = None
        if bukti_id == "":
            bukti_id = None
        try:
            skp_obj = SasaranKinerja.objects.get(pk=skp)
        except SasaranKinerja.DoesNotExist:
            respon = {'success': False, 'pesan': "SKP Tidak ditemukan"}
            return JsonResponse(respon, safe=False)

        try:
            rhk_obj = RencanaHasilKerja.objects.get(pk=rhk)
        except RencanaHasilKerja.DoesNotExist:
            respon = {'success': False, 'pesan': "RHK Tidak ditemukan"}
            return JsonResponse(respon, safe=False)

        if skp_obj and rhk_obj:
            tambah = True
            try:
                obj = BuktiDukung.objects.get(pk=bukti_id)
                tambah = False
            except Exception as e:
                print(e)
                obj = BuktiDukung(
                    skp=skp_obj,
                    rhk=rhk_obj,
                    periode=int(periode)
                )

            obj.nama_bukti_dukung = bukti_dukung
            obj.link = link
            obj.save()

            if tambah:
                respon = {'success': True, 'pesan': "Berhasil Menambah Bukti Dukung"}
            else:
                respon = {'success': True, 'pesan': "Berhasil Merubah Bukti Dukung"}
        return JsonResponse(respon, safe=False)

    def view_bukti_dukung_skp(self, request, skp_id, periode):
        obj = get_object_or_404(SasaranKinerja, pk=skp_id)
        rhk_list = RencanaHasilKerja.objects.filter(
            skp=obj,
        )
        penilai = False
        view = request.GET.get('view', None)
        if view == "penilai":
            penilai = True
        extra_context = {
            "title": "Bukti Dukung",
            "obj": obj,
            "pegawai": obj.pegawai,
            "penilai": obj.pejabat_penilai,
            "rhk_list": rhk_list,
            "penilai_view": penilai,
            "periode": periode,
        }
        return render(
            request, "admin/skp/buktidukung/bukti_dukung.html", extra_context
        )

    def bukti_dukung_delete(self, reqeust, id):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        try:
            obj = BuktiDukung.objects.get(pk=id)
        except BuktiDukung.DoesNotExist:
            respon = {'success': False, 'pesan': "Bukti Dukung Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {
                'success': True,
                'pesan': "Berhasil Menghapus Bukti Dukung"
            }
        return JsonResponse(respon, safe=False)

    def view_cetak_bukti_dukung_pegawai(self, request, obj_id, periode):
        obj = get_object_or_404(SasaranKinerja, pk=obj_id)
        rhk_list = RencanaHasilKerja.objects.filter(
            skp=obj,
        )
        show_ttd = True
        if obj.status in [SasaranKinerja.Status.DRAFT, SasaranKinerja.Status.PENGAJUAN]:
            show_ttd = False
        try:
            nama_pegawai = obj.detailsasarankinerja.nama_pegawai
        except Exception as e:
            print(e)
            nama_pegawai = obj.pegawai.get_complete_name()
        extra_context = {
            "obj": obj,
            "pegawai": obj.pegawai,
            "penilai": obj.pejabat_penilai,
            "title": "Cetak Bukti Dukung {} [{}]".format(
                nama_pegawai, obj.get_periode()
            ),
            "rhk_list": rhk_list,
            "show_ttd": show_ttd,
            "periode": periode
        }
        return render(request, "admin/skp/buktidukung/cetak.html", extra_context)

    def get_urls(self):
        admin_url = super(BuktiDukungAdmin, self).get_urls()
        custom_url = [
            path(
                "<int:skp_id>/bukti-dukung/<int:periode>",
                self.admin_site.admin_view(self.view_bukti_dukung_skp),
                name="bukti-dukung-skp",
            ),
            path(
                "create",
                self.admin_site.admin_view(self.create),
                name="bukti-dukung-create",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.bukti_dukung_delete),
                name="skp_buktidukung_hapus",
            ),
            path(
                "<int:obj_id>/cetak/<int:periode>",
                self.admin_site.admin_view(self.view_cetak_bukti_dukung_pegawai),
                name="skp_buktidukung_cetak",
            ),
        ]
        return custom_url + admin_url
