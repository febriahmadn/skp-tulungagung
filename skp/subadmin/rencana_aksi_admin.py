from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import path

from skp.models import RencanaAksi, RencanaHasilKerja, SasaranKinerja


class RencanaAksiAdmin(admin.ModelAdmin):
    list_display = ("pk", "rhk", "skp", "periode", "rencana_aksi", "created")

    def create(self, request):
        respon = {'success': False}
        skp = request.POST.get('skp_id')
        rencana = request.POST.get('rencana_id')
        periode = request.POST.get('periode')
        rhk = request.POST.get('rhk_id')
        rencana_aksi = request.POST.get('rencana_aksi', None)
        skp_obj = None
        rhk_obj = None
        if rencana == "":
            rencana = None
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
                obj = RencanaAksi.objects.get(pk=rencana)
                tambah = False
            except Exception as e:
                print(e)
                obj = RencanaAksi(
                    skp=skp_obj,
                    rhk=rhk_obj,
                    periode=int(periode)
                )

            obj.rencana_aksi = rencana_aksi
            obj.save()

            if tambah:
                respon = {'success': True, 'pesan': "Berhasil Menambah Rencana Aksi"}
            else:
                respon = {'success': True, 'pesan': "Berhasil Merubah Rencana Aksi"}
        return JsonResponse(respon, safe=False)

    # def view_rencana_aksi_skp(self, request, skp_id, periode):
    def view_rencana_aksi_skp(self, request, skp_id):
        obj = get_object_or_404(SasaranKinerja, pk=skp_id)
        rhk_list = RencanaHasilKerja.objects.filter(
            skp=obj,
        )
        penilai = False
        view = request.GET.get('view', None)
        if view == "penilai":
            penilai = True
        extra_context = {
            "title": "Rencana Aksi",
            "obj": obj,
            "rhk_list": rhk_list,
            "penilai_view": penilai,
            # "periode": periode,
        }
        return render(
            request, "admin/skp/rencanaaksi/rencana_aksi.html", extra_context
        )

    def rencana_delete(self, reqeust, id):
        respon = {'success': False, 'pesan': "Terjadi kesalahan sistem"}
        try:
            obj = RencanaAksi.objects.get(pk=id)
        except RencanaAksi.DoesNotExist:
            respon = {'success': False, 'pesan': "Rencana Aksi Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)
        except Exception as e:
            respon = {'success': False, 'pesan': str(e)}
            return JsonResponse(respon, safe=False)
        else:
            obj.delete()
            respon = {
                'success': True,
                'pesan': "Berhasil Menghapus Rencana Aksi"
            }
        return JsonResponse(respon, safe=False)

    # def view_cetak_rencana_aksi_pegawai(self, request, obj_id, periode):
    def view_cetak_rencana_aksi_pegawai(self, request, obj_id):
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
            "title": "Cetak Rencana Aksi {}".format(
                nama_pegawai
            ),
            "rhk_list": rhk_list,
            "show_ttd": show_ttd,
            # "periode": periode
        }
        return render(request, "admin/skp/rencanaaksi/cetak.html", extra_context)

    def get_urls(self):
        admin_url = super(RencanaAksiAdmin, self).get_urls()
        custom_url = [
            path(
                "<int:skp_id>/rencana-aksi",
                self.admin_site.admin_view(self.view_rencana_aksi_skp),
                name="rencana-aksi-skp",
            ),
            path(
                "create",
                self.admin_site.admin_view(self.create),
                name="rencana-aksi-create",
            ),
            path(
                "<int:id>/hapus",
                self.admin_site.admin_view(self.rencana_delete),
                name="skp_rencanaaksi_hapus",
            ),
            path(
                "<int:obj_id>/cetak",
                self.admin_site.admin_view(self.view_cetak_rencana_aksi_pegawai),
                name="skp_rencanaaksi_cetak",
            ),
        ]
        return custom_url + admin_url
