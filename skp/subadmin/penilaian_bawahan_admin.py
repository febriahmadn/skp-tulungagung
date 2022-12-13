import base64
import datetime

from django.contrib import admin, messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import path, reverse

from skp.models import Hasil, PenilaianBawahan, PerilakuKerja, SasaranKinerja
from usom.models import Account


class PenilaianBawahanAdmin(admin.ModelAdmin):
    def create(self, request):
        respon = {"success": False, "pesan": "Terjadi Kesalahan Sistem"}
        skp_id = request.POST.get("skp_id", None)
        jenis = request.POST.get("jenis", None)
        penilaianbawahan = request.POST.get("penilaianbawahan", None)
        periode = request.POST.get("periode", None)
        hasil = request.POST.get("hasil", None)
        if penilaianbawahan == "":
            penilaianbawahan = None

        try:
            skp_obj = SasaranKinerja.objects.get(pk=skp_id)
        except Exception as e:
            respon = {"success": False, "pesan": str(e)}
            return JsonResponse(respon, safe=False)

        try:
            hasil_obj = Hasil.objects.get(pk=hasil)
        except Exception as e:
            respon = {"success": False, "pesan": str(e)}
            return JsonResponse(respon, safe=False)

        try:
            obj = PenilaianBawahan.objects.get(pk=penilaianbawahan)
        except PenilaianBawahan.DoesNotExist:
            obj = PenilaianBawahan(skp=skp_obj, periode=periode)

        if jenis == "perdikat_perilaku":
            obj.predikat_perilaku = hasil_obj
        elif jenis == "rating_hasil":
            obj.rating_hasil = hasil_obj
        obj.save()

        respon = {"success": True, "pesan": "Berhasil Menambah Hasil"}
        return JsonResponse(respon, safe=False)

    def page_penilaian_bawahan(self, request, skp_id, periode, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )

        b64 = request.GET.get("b64", None)
        awal = None
        akhir = None
        if b64 and b64 != "":
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
        find_all_bawahan = Account.objects.filter(atasan=obj.pegawai)
        extra_context.update(
            {
                "title": "Penilaian Bawahan",
                "periode_penilaian": b64_decode,
                "obj": obj,
                "list_pegawai": find_all_bawahan,
                "awal": awal,
                "akhir": akhir,
                "periode": periode,
            }
        )

        return render(request, "admin/skp/penilaianbawahan/list.html", extra_context)

    def detail_penilaian_bawahan(self, request, skp_id, periode, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect(
                reverse("admin:skp_sasarankinerja_penilaian", kwargs={"id": skp_id})
            )
        perilaku_kerja_list = PerilakuKerja.objects.filter(is_active=True)
        hasil_list = Hasil.objects.filter(is_active=True)
        try:
            penilaian_obj = PenilaianBawahan.objects.get(skp=obj, periode=periode)
        except PenilaianBawahan.DoesNotExist:
            penilaian_obj = None
        except Exception as e:
            print(e)
            penilaian_obj = None

        extra_context.update(
            {
                "title": "Penilaian Bawahan",
                "obj": obj,
                "periode": periode,
                "perilaku_kerja_list": perilaku_kerja_list,
                "hasil_list": hasil_list,
                "penilaian_obj": penilaian_obj,
            }
        )
        return render(request, "admin/skp/penilaianbawahan/detail.html", extra_context)

    def cetak_penilaian_bawahan(self, request, skp_id, periode, extra_context={}):
        try:
            obj = SasaranKinerja.objects.get(pk=skp_id)
        except Exception as e:
            messages.error(request, str(e))
            return redirect(
                reverse("admin:penilaian-bawahan-skp", kwargs={"skp_id": skp_id, 'periode':periode})
            )
        try:
            penilaian_bawah_obj = PenilaianBawahan.objects.get(skp=obj, periode=periode)
        except PenilaianBawahan.DoesNotExist:
            penilaian_bawah_obj = None
        extra_context.update({
            'title':"Penilaian Bawahan",
            'periode':periode,
            'obj':obj,
            "penilaianbawah": penilaian_bawah_obj,
            "perilaku_kerja_list": PerilakuKerja.objects.filter(is_active=True)
            
        })
        return render(request, "admin/skp/penilaianbawahan/cetak.html", extra_context)

    def get_urls(self):
        admin_url = super(PenilaianBawahanAdmin, self).get_urls()
        custom_url = [
            path(
                "<int:skp_id>/penilaian-bawahan/<int:periode>",
                self.admin_site.admin_view(self.page_penilaian_bawahan),
                name="penilaian-bawahan-skp",
            ),
            path(
                "<int:skp_id>/penilaian-bawahan/<int:periode>/detail",
                self.admin_site.admin_view(self.detail_penilaian_bawahan),
                name="penilaian-bawahan-skp-detail",
            ),
            path(
                "<int:skp_id>/penilaian-bawahan/<int:periode>/cetak",
                self.admin_site.admin_view(self.cetak_penilaian_bawahan),
                name="penilaian-bawahan-skp-cetak",
            ),
            path(
                "create",
                self.admin_site.admin_view(self.create),
                name="penilaian-bawahan-create",
            ),
        ]
        return custom_url + admin_url
