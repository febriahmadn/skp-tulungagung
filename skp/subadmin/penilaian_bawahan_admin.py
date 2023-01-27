import base64
import datetime

import xlwt
from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse

from skp.models import Hasil, PenilaianBawahan, PerilakuKerja, SasaranKinerja
from skp.utils import get_predikat_kerja


class PenilaianBawahanAdmin(admin.ModelAdmin):
    def create(self, request):
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        skp_id = request.POST.get("skp_id", None)
        jenis = request.POST.get("jenis", None)
        penilaianbawahan = request.POST.get("penilaianbawahan", None)
        hasil = request.POST.get("hasil", None)

        try:
            skp_obj = SasaranKinerja.objects.get(pk=skp_id)
        except SasaranKinerja.DoesNotExist:
            respon = {"success": False, "pesan": "Sasaran Kinerja Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)

        try:
            hasil_obj = Hasil.objects.get(pk=hasil)
        except Hasil.DoesNotExist:
            respon = {"success": False, "pesan": "Hasil Tidak Ditemukan"}
            return JsonResponse(respon, safe=False)

        try:
            obj = PenilaianBawahan.objects.get(pk=penilaianbawahan)
        except PenilaianBawahan.DoesNotExist:
            obj = PenilaianBawahan(skp=skp_obj)

        if jenis == "perdikat_perilaku":
            obj.predikat_perilaku = hasil_obj
        elif jenis == "rating_hasil":
            obj.rating_hasil = hasil_obj

        obj.predikat_kerja = get_predikat_kerja(
            obj.rating_hasil.nama if obj.rating_hasil else None,
            obj.predikat_perilaku.nama if obj.predikat_perilaku else None,
        )
        if obj.predikat_kerja:
            obj.is_dinilai = True
        obj.save()

        respon = {"success": True, "pesan": "Berhasil Menambah Hasil"}
        return JsonResponse(respon, safe=False)

    def return_awal_akhir(self, request, b64, skp_id):
        awal = None
        akhir = None
        b64_decode = None
        try:
            b64_decode = base64.b64decode(b64).decode("UTF-8")
            text = b64_decode.split("/")
            awal = datetime.datetime.strptime(text[0].strip(), "%Y-%m-%d")
            akhir = datetime.datetime.strptime(text[1].strip(), "%Y-%m-%d")
        except Exception as e:
            messages.error(request, str(e))
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )
        return awal, akhir, b64_decode

    def page_penilaian_bawahan(self, request, skp_id, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except SasaranKinerja.DoesNotExist:
            messages.error(request, "Sasaran Kinerja Tidak Ditemukan")
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )

        b64 = request.GET.get("b64", None)
        cari = request.GET.get("cari", None)
        status = request.GET.get("status", None)
        unit_kerja = request.GET.get("unit_kerja", None)
        awal = None
        akhir = None
        if b64 and b64 != "":
            awal, akhir, b64_decode = self.return_awal_akhir(request, b64, skp_id)
        penilaian_list = PenilaianBawahan.objects.filter(
            skp__induk=obj
        )
        if cari:
            penilaian_list = penilaian_list.filter(
                Q(skp__detailsasarankinerja__nip_pegawai__icontains=cari)
                | Q(skp__detailsasarankinerja__nama_pegawai__icontains=cari)
            )
        if unit_kerja:
            penilaian_list = penilaian_list.filter(skp__unor__id=unit_kerja)

        if status == "2":
            penilaian_list = penilaian_list.filter(is_dinilai=True)
        elif status == "1":
            penilaian_list = penilaian_list.filter(is_dinilai=False)

        status_list = (
            (0, "Semua"),
            (1, "Belum Dinilai"),
            (2, "Sudah Dinilai"),
        )
        is_bupati = False
        if request.user.groups.filter(name="Bupati").exists():
            is_bupati = True
        extra_context.update(
            {
                "title": "Penilaian Bawahan",
                "periode_penilaian": b64_decode,
                "obj": obj,
                "penilaian_list": penilaian_list,
                "awal": awal,
                "akhir": akhir,
                "status_choices": status_list,
                "is_bupati": is_bupati,
            }
        )

        return render(request, "admin/skp/penilaianbawahan/list.html", extra_context)

    def detail_penilaian_bawahan(self, request, skp_id, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except SasaranKinerja.DoesNotExist:
            messages.error(request, "Sasaran Kinerja Tidak Ditemukan")
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )
        perilaku_kerja_list = PerilakuKerja.objects.filter(is_active=True)
        hasil_list = Hasil.objects.filter(is_active=True)
        try:
            penilaian_obj = PenilaianBawahan.objects.get(skp=obj)
        except PenilaianBawahan.DoesNotExist:
            penilaian_obj = None
        except Exception as e:
            print(e)
            penilaian_obj = None

        extra_context.update(
            {
                "title": "Penilaian Bawahan",
                "obj": obj,
                "perilaku_kerja_list": perilaku_kerja_list,
                "hasil_list": hasil_list,
                "penilaian_obj": penilaian_obj,
            }
        )
        return render(request, "admin/skp/penilaianbawahan/detail.html", extra_context)

    def cetak_penilaian_bawahan(self, request, skp_id, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except SasaranKinerja.DoesNotExist:
            messages.error(request, "Sasaran Kinerja Tidak Ditemukan")
            return redirect(
                reverse(
                    "admin:skp_penilaianbawahan",
                    kwargs={"skp_id": skp_id},
                )
            )
        try:
            penilaian_bawah_obj = PenilaianBawahan.objects.get(skp=obj)
        except PenilaianBawahan.DoesNotExist:
            penilaian_bawah_obj = None
        extra_context.update(
            {
                "title": "Penilaian Bawahan",
                "obj": obj,
                "penilaianbawah": penilaian_bawah_obj,
                "perilaku_kerja_list": PerilakuKerja.objects.filter(is_active=True),
            }
        )
        return render(request, "admin/skp/penilaianbawahan/cetak.html", extra_context)

    def form_cetak_penilaian(self, request, skp_id, extra_context={}):
        obj = get_object_or_404(SasaranKinerja, pk=skp_id)
        try:
            penilaian_bawah_obj = PenilaianBawahan.objects.get(skp=obj)
        except PenilaianBawahan.DoesNotExist:
            penilaian_bawah_obj = None
        extra_context.update(
            {
                "title": "Form Penilaian",
                "obj": obj,
                "penilaianbawah": penilaian_bawah_obj,
                "perilaku_kerja_list": PerilakuKerja.objects.filter(is_active=True),
                "predikat_kerja": PenilaianBawahan.PredikatKerja.choices,
            }
        )
        return render(
            request, "admin/skp/penilaianbawahan/form_cetak.html", extra_context
        )

    def export_view(self, request, skp_id, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )
        penilaian_list = PenilaianBawahan.objects.filter(
            skp__induk=obj
        )
        download = request.GET.get("download", None)
        if download == "true":
            filename = "Rekap Penilaian Bawahan {}".format(
                datetime.datetime.now().strftime("%d-%m-%Y")
            )
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = (
                'attachment; filename="' + filename + '.xls"'
            )
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("sheet 1")
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = [
                "NIP",
                "Nama",
                "Jabatan",
                "Rating Hasil Kinerja",
                "Rating Perilaku Kerja",
                "Predikat Perilaku Periodik",
            ]
            rows = []
            for i in penilaian_list:
                isi = (
                    i.skp.detailsasarankinerja.nip_pegawai,
                    i.skp.detailsasarankinerja.nama_pegawai,
                    i.skp.detailsasarankinerja.jabatan_pegawai,
                    i.rating_hasil.nama if i.rating_hasil else "",
                    i.predikat_perilaku.nama if i.predikat_perilaku else "",
                    i.get_predikat_kerja_display().title() if i.predikat_kerja else "",
                )
                rows.append(isi)

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()

            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            return response

        extra_context.update(
            {
                "title": "Rekap Penilaian Bawahan",
                "obj": obj,
                "penilaian_list": penilaian_list,
            }
        )
        return render(request, "admin/skp/penilaianbawahan/export.html", extra_context)

    def kurva_view(self, request, skp_id, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )
        penilaian_list = PenilaianBawahan.objects.filter(
            skp__induk=obj
        )
        data = {
            "sangat_kurang": penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.SANGAT_KURANG
            ).count()
            if penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.SANGAT_KURANG
            ).count()
            >= 1
            else 0,
            "butuh_perbaikan": penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.BUTUH_PERBAIKAN
            ).count()
            if penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.BUTUH_PERBAIKAN
            ).count()
            >= 1
            else 0,
            "kurang": penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.KURANG
            ).count()
            if penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.KURANG
            ).count()
            >= 1
            else 0,
            "baik": penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.BAIK
            ).count()
            if penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.BAIK
            ).count()
            >= 1
            else 0,
            "sangat_baik": penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.SANGAT_BAIK
            ).count()
            if penilaian_list.filter(
                predikat_kerja=PenilaianBawahan.PredikatKerja.SANGAT_BAIK
            ).count()
            >= 1
            else 0,
        }
        extra_context.update(
            {
                "title": "Sasaran Kinerja Pegawai",
                "obj": obj,
                "penilaian_list": penilaian_list,
                "jumlah": data,
            }
        )
        # "penilaian_list": penilaian_list,
        return render(request, "admin/skp/penilaianbawahan/kurva.html", extra_context)

    def get_urls(self):
        admin_url = super(PenilaianBawahanAdmin, self).get_urls()
        custom_url = [
            path(
                "<int:skp_id>/penilaian-bawahan",
                self.admin_site.admin_view(self.page_penilaian_bawahan),
                name="skp_penilaianbawahan",
            ),
            path(
                "<int:skp_id>/penilaian-bawahan/detail",
                self.admin_site.admin_view(self.detail_penilaian_bawahan),
                name="skp_penilaianbawahan_detail",
            ),
            path(
                "<int:skp_id>/penilaian-bawahan/cetak",
                self.admin_site.admin_view(self.cetak_penilaian_bawahan),
                name="skp_penilaianbawahan_cetak",
            ),
            path(
                "<int:skp_id>/form-penilaian/cetak",
                self.admin_site.admin_view(self.form_cetak_penilaian),
                name="skp_penilaianbawahan_formpenilaiancetak",
            ),
            path(
                "<int:skp_id>/penilaian-bawahan/export",
                self.admin_site.admin_view(self.export_view),
                name="skp_penilaianbawahan_export",
            ),
            path(
                "<int:skp_id>/penilaian-bawahan/kurva",
                self.admin_site.admin_view(self.kurva_view),
                name="skp_penilaianbawahan_kurva",
            ),
            path(
                "create",
                self.admin_site.admin_view(self.create),
                name="skp_penilaianbawahan_create",
            ),
        ]
        return custom_url + admin_url
